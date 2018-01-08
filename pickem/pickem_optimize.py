import csv
import random
import requests
import numpy
from terminaltables import AsciiTable
from draft_kings_db import client
from pickem.pickem_orm import TieredLineup, TieredPlayer, TIERS
from pickem import pickem_upload


def optimize(all_players):
    lineup_players = []
    for t in TIERS:
        best = sorted(
            [p for p in all_players if p.tier == t],
            key=lambda p: p.proj,
            reverse=True,
        )[0]
        lineup_players.append(best)

    return TieredLineup(lineup_players)


def get_all_players(pickem_file_location):
    all_players = []
    with open(pickem_file_location) as csv_file:
        reader = csv.DictReader(csv_file)
        player_data = requests.get(
            'https://mom-api.herokuapp.com/content/players/?league =NBA'
        ).json()['players']
        for row in reader:
            all_players.append(
                TieredPlayer(
                    cost=0,  # salary not applicable in pickem
                    name=row['Name'],
                    pos=row['Position'],
                    team=row['teamAbbrev'],
                    matchup=row['GameInfo'],
                    proj=next(
                        p for p in player_data
                        if p['name'] == row['Name']
                    )['proj'],
                    average_score=float(row['AvgPointsPerGame']),
                    tier=row['Roster_Position']
                )
            )
    return all_players


def run(pickem_file_location):
    all_players = get_all_players(pickem_file_location)
    roster = optimize(all_players)
    print(roster)


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


def review_past(file_loc, banned):
    '''
    Prints out results from a previous slate with variance (numpy.std)
    for each tier.

    :param file_loc: Salaries file from already played games
    :param banned: Players to not include (injured or missed game)
    '''
    c = client.DraftKingsHistory()
    c.initialize_nba()
    players = get_all_players(file_loc)
    for t in TIERS:
        headers = [[
            'Name',
            'Actual',
            'Tier'
        ]]
        tp = [p for p in players if p.tier == t and p.name not in banned]
        body_data = []
        for tpl in tp:
            actual = c.lookup_nba_performances(tpl.name)[0].draft_kings_points
            body_data += [[tpl.name, actual, tpl.tier]]

        sorted_body = sorted(body_data, key=lambda x: x[1], reverse=True)

        print(t)
        print(AsciiTable(headers + sorted_body).table)
        print('Variance: {}'.format(numpy.std([g[1] for g in body_data])))
        print('***********')
        print('')
