import csv
from draftfast.orm import Player
from draftfast.rules import DRAFT_KINGS, FAN_DUEL

GAME_KEY_MAP = {
    DRAFT_KINGS: {
        'name': 'Name',
        'salary': 'Salary',
        'team': 'teamAbbrev',
        'team_alt': 'TeamAbbrev',
        'game': 'GameInfo',
        'game_alt': 'Game Info',
        'avg': 'AvgPointsPerGame',
    },
    FAN_DUEL: {
        'name': 'Nickname',
        'team': 'Team',
        'team_alt': None,
        'game': 'Game',
        'game_alt': None,
        'avg': 'FPPG',
    }
}


# TODO - return players given two CSV locations and RuleSet
# The two CSVs here should be 1) the DK / FD salary sheet
# and 2) player projections
def generate_players_from_csvs(
    salary_file_location: str,
    game: str,
    projection_file_location='',
    verbose=False,
) -> list:
    players = []
    projections = None
    if projection_file_location:
        projections = _generate_projection_dict(
            projection_file_location
        )

    with open(salary_file_location, 'r') as csv_file:
        csv_data = csv.DictReader(csv_file)
        for row in csv_data:
            for pos in row['Position'].split('/'):
                player = generate_player(
                    pos=pos,
                    row=row,
                    game=game,
                )
                if projections:
                    proj = projections.get(player.name)
                    if proj is None:
                        if verbose:
                            print('No projection for {}'.format(player.name))
                        player.proj = 0
                    else:
                        player.proj = proj
                else:
                    player.proj = player.average_score

                players.append(player)

    return players


def generate_player(pos, row, game):
    '''
    Parses CSV row for DraftKings or FanDuel
    and returns a player. Note that DraftKings
    has different CSV formats for different
    sports.
    '''
    avg_key = GAME_KEY_MAP[game]['avg']
    name_key = GAME_KEY_MAP[game]['name']
    team_key = GAME_KEY_MAP[game]['team']
    team_alt_key = GAME_KEY_MAP[game]['team_alt']
    game_key = GAME_KEY_MAP[game]['game']
    game_alt_key = GAME_KEY_MAP[game]['game_alt']

    avg = float(row.get(avg_key, 0))

    player = Player(
        pos,
        row[name_key],
        row['Salary'],
        possible_positions=row['Position'],
        multi_position='/' in row['Position'],
        team=row.get(team_key) or row.get(team_alt_key),
        matchup=row.get(game_key) or row.get(game_alt_key),
        average_score=avg,
    )

    return player


def _generate_projection_dict(projection_file_location: str) -> dict:
    projections = {}
    with open(projection_file_location, 'r') as csv_file:
        csv_data = csv.DictReader(csv_file)
        for row in csv_data:
            projections[row.get('playername')] = float(row.get('points'))

    return projections
