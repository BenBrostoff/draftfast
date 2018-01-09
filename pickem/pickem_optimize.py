import csv
import random
from terminaltables import AsciiTable
from draft_kings_db import client
from query_constraints import add_pickem_contraints
from pickem.pickem_orm import TieredLineup, TieredPlayer, TIERS
from pickem import pickem_upload


def optimize(all_players, cmd_args=None):
    lineup_players = []
    all_players = filter(
        add_pickem_contraints(cmd_args),
        all_players
    )
    for t in TIERS:
        best = sorted(
            [p for p in all_players if p.tier == t],
            key=lambda p: p.proj,
            reverse=True,
        )[0]
        lineup_players.append(best)

    return TieredLineup(lineup_players)


def get_all_players(
    pickem_file_location,
    projection_file,
    use_averages
):
    all_players = []
    if projection_file:
        projection_map = _get_projection_map(projection_file)

    with open(pickem_file_location) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if use_averages:
                proj = float(row['AvgPointsPerGame'])
            else:
                try:
                    proj = float(projection_map[row['Name']])
                except KeyError:
                    print(
                        'No projection provided for {}. '
                        'Setting points to 0.'
                    ).format(row['Name'])
                    proj = 0

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


def upload(pickem_file_location, map_file_location, lineup_nums=10):
    pickem_upload.create_upload_file()
    player_map = pickem_upload.map_pids(map_file_location)
    all_players = get_all_players(pickem_file_location)

    for _ in range(lineup_nums):
        # TODO - move to example
        random_lineup = []
        for t in TIERS:
            random_lineup.append(
                random.choice(
                    [p for p in all_players if p.tier == t]
                )
            )
        pickem_upload.update_upload_csv(
            player_map,
            TieredLineup(random_lineup)
        )


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

    players = get_all_players(file_loc)
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
