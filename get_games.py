import csv

from orm import Game


def get_games():
    all_games = []
    with open('data/current-salaries.csv', 'r') as csvfile:
        csvdata = csv.DictReader(csvfile)
        for idx, row in enumerate(csvdata):
            if idx > 0:
                team = row['GameInfo'].split('@')[0].upper()
                opp = row['GameInfo'].split('@')[1].split(' ')[0].upper()
                if not any(map(lambda x: x.team_in_game(team), all_games)):
                    all_games.append(Game(team, opp))
    return all_games
