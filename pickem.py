import sys
import csv
from orm import Player
from terminaltables import AsciiTable
import requests

TIERS = [
    'T1',
    'T2',
    'T3',
    'T4',
    'T5',
    'T6',
]


class TieredLineup(object):

    def __init__(self, players):
        self.players = players

    def __repr__(self):
        table_data = [[
            'Name',
            'Tier',
            'Matchup',
            'Projected',
            'vs Avg',
        ]]
        for p in self.players:
            table_data.append(p.to_table_row())
        return (
            AsciiTable(table_data).table +
            '\n' +
            'Total: {}'.format(self.total)
        )

    @property
    def total(self):
        return sum([p.proj for p in self.players])


class TieredPlayer(Player):

    def __init__(self, tier, **kwargs):
        self.tier = tier
        super(TieredPlayer, self).__init__(
            **kwargs
        )

    def to_table_row(self):
        return [
            self.name,
            self.tier,
            self.matchup,
            self.proj,
            self.v_avg,
        ]


def optimize(all_players):
    lineup_players = []
    for t in TIERS:
        best = sorted(
            [p for p in all_players if p.tier == t],
            key=lambda p: p.proj,
            reverse=True,
        )[0]
        lineup_players.append(best)

    print(TieredLineup(lineup_players))


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


run(sys.argv[1])
