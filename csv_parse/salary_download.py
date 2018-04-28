from orm import Player
from constants import DRAFT_KINGS, FAN_DUEL

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


def generate_player(pos, row, args):
    '''
    Parses CSV row for DraftKings or FanDuel
    and returns a player. Note that DraftKings
    has different CSV formats for different
    sports.
    '''
    avg_key = GAME_KEY_MAP[args.game]['avg']
    name_key = GAME_KEY_MAP[args.game]['name']
    team_key = GAME_KEY_MAP[args.game]['team']
    team_alt_key = GAME_KEY_MAP[args.game]['team_alt']
    game_key = GAME_KEY_MAP[args.game]['game']
    game_alt_key = GAME_KEY_MAP[args.game]['game_alt']

    avg = float(row.get(avg_key, 0))

    player = Player(
        pos,
        row[name_key],
        row['Salary'],
        possible_positions=row['Position'],
        multi_position=('/' in row['Position']),
        team=row.get(team_key) or row.get(team_alt_key),
        matchup=row.get(game_key) or row.get(game_alt_key),
        average_score=avg,
        lock=(args.locked and row[name_key] in args.locked)
    )

    if args.source == 'DK_AVG':
        player.proj = avg

    return player
