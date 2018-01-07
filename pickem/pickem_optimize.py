import csv
import requests
from pickem.pickem_orm import TieredLineup, TieredPlayer, TIERS


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


def run(pickem_file_location):
    player_data = requests.get(
        'https://mom-api.herokuapp.com/content/players/?league =NBA'
    ).json()['players']
    with open(pickem_file_location) as csv_file:
        reader = csv.DictReader(csv_file)
        all_players = []
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

    return optimize(all_players)
