from collections import Counter
from typing import List, Dict
import locale
from terminaltables import AsciiTable
from functools import total_ordering
import re

try:
    locale.setlocale(locale.LC_ALL, "en_US")
except Exception:
    pass


def cs(n):
    return locale._format("%d", n, grouping=True)


@total_ordering
class Player(object):
    def __init__(
        self,
        pos,
        name,
        cost,
        proj=0,
        projected_ownership_pct=0,
        lineup_count=0,
        average_score=0,
        matchup=None,
        team=None,
        marked=None,
        possible_positions=None,
        lock=False,
        position_lock=False,
        ban=False,
        multi_position=False,
        kv_store={},
    ):
        self.pos = pos
        self.name = name
        self.cost = float(cost)
        self.team = team.upper() if team else team
        self.matchup = matchup
        self.proj = proj
        self.average_score = average_score
        self.projected_ownership_pct = projected_ownership_pct
        self.lineup_count = lineup_count
        self.marked = marked
        self.lock = lock
        self.position_lock = position_lock
        self.ban = ban
        self.position_ban = False
        self.multi_position = multi_position
        self.possible_positions = possible_positions
        self.kv_store = kv_store

    def get_player_id(self, player_map):
        return player_map[self.name + " " + self.possible_positions]

    def to_table_row(self):
        return [
            self.formatted_position,
            self.name,
            self.team,
            self.matchup,
            cs(self.cost),
            self.proj,
            self.__format_v_avg(),
            "LOCK" if self.lock else "",
        ]

    def to_exposure_table_row(self, n, s_min, s_max):
        return [
            self.formatted_position,
            self.name,
            self.team,
            self.matchup,
            cs(self.cost),
            self.proj,
            n,
            s_min,
            s_max,
        ]

    def is_opposing_team_in_match_up(self, team):
        return (team.upper() != self.team.upper()) and (
            team.upper() in self.matchup.upper()
        )

    def __repr__(self):
        v_avg = self.__format_v_avg()
        player_dict = dict(
            pos=self.formatted_position,
            name=self.name,
            team=self.team,
            match=self.matchup,
            cost=cs(self.cost),
            proj=self.proj,
            v_avg=v_avg,
            lock="LOCK" if self.lock else "",
        )

        return (
            "[{pos: <2}] {name: <20} {team} {match} "
            "(${cost}, {proj} ({v_avg})), {lock}".format(**player_dict)
        )

    def __eq__(self, player):
        return (
            self.pos == player.pos
            and self.name == player.name
            and self.cost == player.cost
            and self.team == player.team
        )

    def __hash__(self):
        return hash((self.pos, self.name, self.cost, self.team))

    def __lt__(self, player):
        if self.cost == player.cost:
            return self.name < player.name
        return self.cost < player.cost

    @property
    def value(self):
        return round(self.proj / (self.cost / 1000), 2)

    @property
    def solver_id(self):
        """
        Used by optimizer to accommodate same player in different positions
        """
        return f"{self.name} {self.pos} {self.team}"

    @property
    def roster_id(self):
        """
        Used for roster equality. From the perspective of someone
        entering lineups,a lineup with the same players scores
        the same points irrespective of positions
        """
        return f"{self.name} {self.team}"

    @property
    def formatted_position(self):
        if self.multi_position:
            return f"{self.possible_positions} ({self.pos})"
        return self.pos

    @property
    def v_avg(self):
        return self.proj - self.average_score

    @property
    def is_home(self):
        match_up_teams = self.matchup.split(" ")[0]
        return self.team == match_up_teams.split("@")[-1]

    @property
    def nba_general_position(self):
        if self.pos == "SG" or self.pos == "PG" or self.pos == "G":
            return "G"
        elif self.pos == "SF" or self.pos == "PF" or self.pos == "F":
            return "F"
        return "C"

    @property
    def mlb_general_position(self):
        if self.pos in {"SP", "RP"}:
            return "P"
        return self.pos

    @property
    def short_name(self):
        s = self.name.split()

        # DST
        if len(s) == 1:
            return self.name

        # like "AJ McCarron"
        if re.match(r"^[A-Z]{2}$", s[0]):
            return s

        return f"{s[0][0]}. {s[1]}"

    def __set_from_data_cache(self, player_data):
        if player_data is None:
            return
        for k, v in list(player_data.items()):
            setattr(self, k, v)

    def __format_v_avg(self):
        if self.v_avg > 0:
            return "\x1b[0;32;40m{:0.2f}\x1b[0m".format(self.v_avg)
        return "\x1b[0;31;40m{:0.2f}\x1b[0m".format(self.v_avg)


class Roster:
    def __init__(self):
        self.players = []
        self.cached_id = None

    def __repr__(self):
        table_data = []
        headers = [
            "Position",
            "Player",
            "Team",
            "Matchup",
            "Salary",
            "Projection",
            "vs. Avg.",
            "Locked",
        ]
        table_data.append(headers)
        for p in self.sorted_players():
            table_data.append(p.to_table_row())

        table = AsciiTable(table_data)
        table.justify_columns[4] = "right"
        table.justify_columns[5] = "right"
        table.justify_columns[6] = "right"

        aggregate_info = "\n\nProjected Score: {:0.2f} \t Cost: ${}".format(
            self.projected(), cs(self.spent())
        )

        return table.table + aggregate_info

    @property
    def identifier(self):
        if self.cached_id:
            return self.cached_id
        self.cached_id = " ".join(
            sorted([x.roster_id for x in self.sorted_players()])
        )

        return self.cached_id

    def __eq__(self, other):
        if not other:
            return False

        return self.identifier == other.identifier

    def __hash__(self):
        return hash(self.identifier)

    def __contains__(self, player):
        if isinstance(player, str):
            for p in self.players:
                if p.name == player or p.short_name == player:
                    return True
        elif isinstance(player, Player):
            return player in self.players
        else:
            raise NotImplementedError()

        return False

    def add_player(self, player):
        self.players.append(player)

    def spent(self):
        return sum([x.cost for x in self.players])

    def projected(self):
        return sum([x.proj for x in self.players])

    def position_order(self, player):
        # raises exception in case someone tries to instantiate base class
        position_order = getattr(self, "POSITION_ORDER")

        # default sort order is low->high, so use the negative of cost
        return position_order[player.pos], -player.cost

    def sorted_players(self):
        return sorted(self.players, key=lambda p: self.position_order(p))

    def different_player_count(self, other_roster):
        dpc = 0
        other_roster_players: List[Player] = other_roster.players
        for player in self.players:
            if player not in other_roster_players:
                dpc += 1
        return dpc

    def shared_player_count(self, other_roster):
        spc = 0
        other_roster_players: List[Player] = other_roster.players
        for player in self.players:
            if player in other_roster_players:
                spc += 1
        return spc


class RosterGroup:
    """
    Group of rosters that might be entered into GPP or other contest.
    The purpose of this class is to allow for easy retrieval of metrics
    that would be helpful for thinking about multi-entry.
    """

    def __init__(self, rosters: List[Roster]):
        self.rosters = rosters

    def get_player_frequency(self):
        players = []
        for r in self.rosters:
            for p in r.players:
                players.append(p)

        counter = Counter(players)
        return sorted(
            counter.items(),
            reverse=True,
            key=lambda items: items[1],
        )

    def get_salary_frequency(self) -> List[Dict[int, int]]:
        salaries = []
        for r in self.rosters:
            salaries.append(r.spent())

        counter = Counter(salaries)
        return sorted(counter.items(), key=lambda items: items[0])

    def get_similarity_score(self):
        """
        A similarity score of 1 means you're playing all of the same lineups.
        0 would all be all different players in all different lineups.
        0.5 would be say 3 lineups of 6 players with three of the same in each.
        """
        scores, pairs = [], []
        for idx, r in enumerate(self.rosters):
            for idx_comp, r_comp in enumerate(self.rosters):
                if idx == idx_comp or (sorted([idx_comp, idx]) in pairs):
                    # Do not compare to self or re-make comparison
                    continue

                if r == r_comp:
                    scores.append(1)
                else:
                    scores.append(self.__get_roster_similarity(r, r_comp))
                pairs.append(sorted([idx_comp, idx]))

        return sum(scores) / len(scores)

    def __get_roster_similarity(self, roster_a, roster_b):
        return roster_a.shared_player_count(roster_b) / len(roster_a.players)


"""
POSITION_ORDER is based on the order
required by DraftKings' CSV download
"""


class ShowdownRoster(Roster):
    POSITION_ORDER = {
        "CPT": 0,
        "FLEX": 1,
    }

    @property
    def identifier(self):
        """
        In Showdown, only two positions exist
        and a change in position means a change
        in points, so unique is on position.
        """
        if self.cached_id:
            return self.cached_id
        self.cached_id = " ".join(
            sorted([x.solver_id for x in self.sorted_players()])
        )

        return self.cached_id


class MVPRoster(ShowdownRoster):
    POSITION_ORDER = {
        # TODO - adjust NFL FD to MVP format
        # and remove CPT, FLEX
        "CPT": 0,
        "MVP": 0,
        "FLEX": 1,
        "STAR": 1,
        "PRO": 2,
        "UTIL": 3,
    }


class NFLRoster(Roster):
    POSITION_ORDER = {
        "QB": 0,
        "RB": 1,
        "WR": 2,
        "TE": 3,
        "DST": 4,
        "D": 5,
    }


class TenRoster(Roster):
    POSITION_ORDER = {
        "P": 1,
    }


class MLBRoster(Roster):
    POSITION_ORDER = {
        "P": 0,
        "RP": 0,
        "SP": 0,
        "C": 1,
        "1B": 2,
        "2B": 3,
        "3B": 4,
        "SS": 5,
        "OF": 6,
    }


class NBARoster(Roster):
    POSITION_ORDER = {"PG": 0, "SG": 1, "SF": 2, "PF": 3, "C": 4}


class WNBARoster(Roster):
    POSITION_ORDER = {
        "G": 0,
        "F": 1,
        "SG": 2,
        "SF": 3,
        "PF": 4,
    }


class NASCARRoster(Roster):
    POSITION_ORDER = {
        "D": 0,
    }


class PGARoster(Roster):
    POSITION_ORDER = {
        "G": 0,
    }


class PGACaptainRoster(Roster):
    POSITION_ORDER = {
        "CPT": 0,
        "G": 1,
    }


class SoccerRoster(Roster):
    POSITION_ORDER = {
        "F": 0,
        "M": 1,
        "D": 2,
        "GK": 3,
    }


class ELRoster(Roster):
    POSITION_ORDER = {
        "G": 0,
        "F": 1,
    }


class NHLRoster(Roster):
    POSITION_ORDER = {
        "C": 0,
        "W": 1,
        "D": 2,
        "G": 3,
    }


class F1ShowdownRoster(Roster):
    POSITION_ORDER = {
        "CPT": 0,
        "D": 1,
        "CNSTR": 2,
    }


class RosterSelect:
    @staticmethod
    def roster_gen(league):
        roster_dict = {
            "NBA": NBARoster(),
            "NBA_SHOWDOWN": ShowdownRoster(),
            "WNBA": WNBARoster(),
            "NFL": NFLRoster(),
            "NFL_SHOWDOWN": ShowdownRoster(),
            "MLB_MVP": MVPRoster(),
            "NBA_MVP": MVPRoster(),
            "NFL_MVP": MVPRoster(),
            "MLB": MLBRoster(),
            "PGA": PGARoster(),
            "PGA_CAPTAIN": PGACaptainRoster(),
            "NASCAR": NASCARRoster(),
            "SOCCER": SoccerRoster(),
            "EL": ELRoster(),
            "NHL": NHLRoster(),
            "NHL_SHOWDOWN": ShowdownRoster(),
            "MLB_SHOWDOWN": ShowdownRoster(),
            # XFL uses the same positions as NFL
            "XFL": NFLRoster(),
            "TEN": TenRoster(),
            "CSGO_SHOWDOWN": ShowdownRoster(),
            "F1_SHOWDOWN": F1ShowdownRoster(),
        }
        return roster_dict[league]


class Game:
    def __init__(self, team, opp):
        self.team = team
        self.opponent = opp

    def __repr__(self):
        return f"{self.team} @ {self.opponent}"

    def team_in_game(self, team):
        return team == self.team or team == self.opponent

    def get_teams(self):
        return self.team, self.opponent
