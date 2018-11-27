import csv
from terminaltables import AsciiTable
from draft_kings_db import client
from draftfast.player_pool import add_pickem_contraints
from draftfast.pickem.pickem_orm import TieredLineup, TieredPlayer, TIERS


def optimize(all_players, cmd_args=None):
    lineup_players = []
    all_players = list(filter(
        add_pickem_contraints(cmd_args),
        all_players
    ))
    for t in TIERS:
        best = sorted(
            [p for p in all_players if p.tier == t],
            key=lambda p: p.proj,
            reverse=True,
        )[0]

        lineup_players.append(best)

    lineup = TieredLineup(lineup_players)
    locked = cmd_args.locked if cmd_args else None
    if locked:
        for lock in locked:
            player_lock = _get_player(lock, all_players)
            player_lock.locked = True
            setattr(
                lineup,
                player_lock.tier,
                player_lock,
            )

    return lineup


def get_all_players(
    pickem_file_location,
    projection_file,
    use_averages=False,
):
    all_players = []
    if projection_file:
        projection_map = _get_projection_map(projection_file)

    with open(pickem_file_location) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if use_averages:
                proj = float(row['AvgPointsPerGame'])
            elif projection_file:
                try:
                    proj = float(projection_map[row['Name']])
                except KeyError:
                    print(
                        'No projection provided for {}. '
                        'Setting points to 0.'
                    ).format(row['Name'])
                    proj = 0
            else:
                proj = float(row['AvgPointsPerGame'])

            all_players.append(
                TieredPlayer(
                    cost=0,  # salary not applicable in pickem
                    name=row['Name'],
                    pos=row['Position'],
                    team=row['teamAbbrev'],
                    matchup=row['GameInfo'],
                    proj=proj,
                    average_score=float(row['AvgPointsPerGame']),
                    tier=row['Roster_Position']
                )
            )
    return all_players


def print_green(txt):
    return '\x1b[0;32;40m{}\x1b[0m'.format(txt)


def review_past(file_loc, banned):
    '''
    Prints out results from a previous slate with variance (numpy.std)
    for each tier.

    :param file_loc: Salaries file from already played games
    :param banned: Players to not include (injured or missed game)
    '''

    # FIXME - this will retrieve data from S3 and store in
    # an in-memory DB. After running this function once on a
    # given day, the data should persist.
    c = client.DraftKingsHistory()
    c.initialize_nba()

    players = get_all_players(file_loc, None, True)
    all_body_data = []
    headers = [[
        'Name',
        'Team',
        'Actual',
        'Tier'
    ]]

    for idx, t in enumerate(TIERS):
        tp = [p for p in players if p.tier == t and p.name not in banned]
        body_data = []

        for tpl in tp:
            actual = c.lookup_nba_performances(tpl.name)[0].draft_kings_points
            body_data += [[tpl.name, tpl.team, round(actual, 2), tpl.tier]]

        sorted_body_data = sorted(body_data, key=lambda x: x[2], reverse=True)
        if idx % 2 != 0:
            sorted_body_data = [
                [print_green(cell) for cell in entry] for
                entry in sorted_body_data
            ]

        all_body_data += sorted_body_data

    print(' ')
    print(
        AsciiTable(headers + all_body_data, title='Pickem Results').table
    )


def _get_projection_map(projection_file):
    '''
    Read from passed CSV file and return map of projections with
    player names as keys.
    '''
    projection_map = {}
    with open(projection_file) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            projection_map[row['playername']] = row['points']

    return projection_map


def _get_player(name, all_players):
    return next(
        p for p in all_players if p.name == name
    )
