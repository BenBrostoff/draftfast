import csv
import os

from orm import Game, Player

salaries_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'current-salaries.csv')

def get_games():
    all_games = []
    with open(salaries_csv, 'r') as csvfile:
        csvdata = csv.DictReader(csvfile)
        for idx, row in enumerate(csvdata):
            if idx > 0:
                team = row['GameInfo'].split('@')[0].upper()
                opp = row['GameInfo'].split('@')[1].split(' ')[0].upper()
                if not any(map(lambda x: x.team_in_game(team), all_games)):
                    all_games.append(Game(team, opp))
    return all_games


def get_all_players():
    all_players = []

    with open(salaries_csv, 'rb') as csvfile:
        csvdata = csv.DictReader(csvfile)

        for idx, row in enumerate(csvdata):
            if idx > 0:
                player = Player(row['Position'], row['Name'], row['Salary'],
                                team=row['teamAbbrev'],
                                matchup=row['GameInfo'])
                all_players.append(player)
    return all_players
