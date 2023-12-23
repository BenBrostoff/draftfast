import csv
from typing import List
from draftfast.orm import Player
from draftfast.pickem.pickem_orm import TieredPlayer
from draftfast.showdown.orm import ShowdownPlayer, MVPPlayer
from draftfast.rules import (
    RuleSet,
    DRAFT_KINGS,
    FAN_DUEL,
    FD_NFL_MVP_RULE_SET,
    FD_MLB_MVP_RULE_SET,
    FD_NBA_MVP_RULE_SET,
)

GAME_KEY_MAP = {
    DRAFT_KINGS: {
        "name": "Name",
        "salary": "Salary",
        "team": "teamAbbrev",
        "team_alt": "TeamAbbrev",
        "game": "GameInfo",
        "game_alt": "Game Info",
        "avg": "AvgPointsPerGame",
    },
    FAN_DUEL: {
        "name": "Nickname",
        "team": "Team",
        "team_alt": None,
        "game": "Game",
        "game_alt": None,
        "avg": "FPPG",
    },
}


# TODO - return players given two CSV locations and RuleSet
# The two CSVs here should be 1) the DK / FD salary sheet
# and 2) player projections
def generate_players_from_csvs(
    salary_file_location: str,
    game: str,
    projection_file_location="",
    verbose=False,
    encoding="utf-8",
    errors="replace",
    ruleset=None,
) -> list:
    players = []
    projections = None
    if projection_file_location:
        projections = _generate_projection_dict(
            projection_file_location,
            encoding,
            errors,
        )

    with open(
        salary_file_location, "r", encoding=encoding, errors=errors
    ) as csv_file:
        csv_data = csv.DictReader(csv_file)
        pos_key = "Position"
        is_nhl = ruleset and ruleset.league == "NHL"
        is_showdown = ruleset and ruleset.game_type == "showdown"
        if is_nhl or is_showdown:
            pos_key = "Roster Position"

        for row in csv_data:
            if ruleset and ruleset.game_type == "pickem":
                player = TieredPlayer(
                    cost=0,  # salary not applicable in pickem
                    name=row["Name"],
                    pos=row["Position"],
                    team=row["TeamAbbrev"],
                    matchup=row["Game Info"],
                    average_score=float(row["AvgPointsPerGame"]),
                    tier=row["Roster Position"],
                )
                _set_projections(
                    projections,
                    player,
                    verbose,
                )
                players.append(player)
            elif ruleset == FD_NFL_MVP_RULE_SET:
                parsed = _parse_fd_mvp_nfl_row(
                    pos=row["Position"],
                    row=row,
                )
                players += parsed
                continue
            elif ruleset in [FD_MLB_MVP_RULE_SET, FD_NBA_MVP_RULE_SET]:
                parsed = _parse_mvp_mlb_row(
                    pos=row["Position"],
                    row=row,
                    ruleset=ruleset,
                )
                players += parsed
                continue
            elif is_showdown:
                pos = row[pos_key]
                player = generate_player(
                    pos=row["Position"],
                    row=row,
                    game=game,
                )
                _set_projections(
                    projections,
                    player,
                    verbose,
                )
                captain = pos == "CPT"

                showdown_pos = None

                # F1 requires unique non-captain position
                if ruleset.league == "F1_SHOWDOWN":
                    showdown_pos = pos if not captain else None

                players.append(
                    ShowdownPlayer(
                        player,
                        pos=showdown_pos if not captain else None,
                        captain=captain,
                    )
                )
            else:
                for pos in row[pos_key].split("/"):
                    if is_nhl and pos == "UTIL":
                        continue
                    player = generate_player(
                        pos=pos,
                        row=row,
                        game=game,
                    )
                    _set_projections(
                        projections,
                        player,
                        verbose,
                    )

                    players.append(player)

    return players


def generate_player(pos, row, game):
    """
    Parses CSV row for DraftKings or FanDuel
    and returns a player. Note that DraftKings
    has different CSV formats for different
    sports.
    """
    avg_key = GAME_KEY_MAP[game]["avg"]
    name_key = GAME_KEY_MAP[game]["name"]
    team_key = GAME_KEY_MAP[game]["team"]
    team_alt_key = GAME_KEY_MAP[game]["team_alt"]
    game_key = GAME_KEY_MAP[game]["game"]
    game_alt_key = GAME_KEY_MAP[game]["game_alt"]
    avg = float(row.get(avg_key, 0) or 0)

    player = Player(
        pos,
        row[name_key].strip().rstrip(),
        row["Salary"],
        possible_positions=row["Position"],
        multi_position="/" in row["Position"],
        team=row.get(team_key) or row.get(team_alt_key),
        matchup=row.get(game_key) or row.get(game_alt_key),
        average_score=avg,
        kv_store=row,
    )

    return player


def _parse_fd_mvp_nfl_row(pos: str, row: dict) -> List[ShowdownPlayer]:
    """
    FanDuel CSVs give all players without breaking out a captain position.
    Unlike DK, salary does not change here.
    To allow DraftFast to correctly optimize, break into two players.
    """
    player = generate_player(
        pos=pos,
        row=row,
        game=FAN_DUEL,
    )
    captain = ShowdownPlayer(
        player,
        captain=True,
    )

    # Unlike DK, FD does not break out players by captain,
    # so make the adjustment here
    captain.average_score *= ShowdownPlayer._CAPTAIN_MULTIPLIER

    return [
        captain,
        ShowdownPlayer(
            player,
            captain=False,
        ),
    ]


def _parse_mvp_mlb_row(
    pos: str, row: dict, ruleset: RuleSet
) -> List[ShowdownPlayer]:
    """
    FanDuel CSVs give all players without breaking out an MVP / STAR position.
    Unlike DK, salary does not change here.
    To allow DraftFast to correctly optimize, break into three players.
    """
    player = generate_player(
        pos=pos,
        row=row,
        game=FAN_DUEL,
    )
    util = MVPPlayer.from_player(player, game_position="UTIL")
    mvp = MVPPlayer.from_player(
        player,
        game_position="MVP",
    )
    star = MVPPlayer.from_player(player, game_position="STAR")

    # Unlike DK, FD does not break out players by multiplier position
    mvp.average_score *= MVPPlayer.MVP_MULTIPLIER
    star.average_score *= MVPPlayer.STAR_MULTIPLIER

    # NBA contains PRO
    if ruleset == FD_NBA_MVP_RULE_SET:
        pro = MVPPlayer.from_player(player, game_position="PRO")
        pro.average_score *= MVPPlayer.PRO_MULTIPLIER
        return [mvp, star, pro, util]

    return [mvp, star, util]


def _generate_projection_dict(
    projection_file_location: str, encoding: str, errors: str
) -> dict:
    projections = {}
    with open(
        projection_file_location, "r", encoding=encoding, errors=errors
    ) as csv_file:
        csv_data = csv.DictReader(csv_file)
        for row in csv_data:
            name = row.get("playername").strip().rstrip()
            projections[name] = float(row.get("points"))

    return projections


def _set_projections(projections, player, verbose):
    if projections:
        proj = projections.get(player.name)

        # try to find projection for e.g. 'Andrew Luck IND'
        if proj is None and player.team is not None:
            alt_name = "{} {}".format(player.name, player.team.upper())
            proj = projections.get(alt_name)

        if proj is None:
            if verbose:
                print("No projection for {}".format(player.name))
            player.proj = 0
        else:
            player.proj = proj
    else:
        player.proj = player.average_score
