import csv
import random
import requests
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
