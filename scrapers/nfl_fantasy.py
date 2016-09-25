import csv
import requests
from bs4 import BeautifulSoup as BS


NFL_FAN_POSITIONS = ['QB', 'RB', 'WR', 'TE', 'DEF']

NFL_FAN_URL = \
    'http://fantasy.nfl.com/research/projections?offset={}&position={}'

DEFAULT_FILE_PATH = 'data/current-nfl-fan-projections.csv'


def scrape(limit=1000, file_path=DEFAULT_FILE_PATH):
    hold = scrape_nfl_fan(limit)
    write_to_csv(hold, file_path)


def scrape_nfl_fan(limit):
    hold = []
    hold.append(['playername', 'points'])
    for i in range(0, limit/25):
        param = (i * 25) + 1
        r = requests.get(NFL_FAN_URL.format(param, 'O'))
        soup = BS(r.text, 'html.parser')
        player_rows = filter(lambda x: x,
                             [x.find_all('td') for x in soup.find_all('tr')])
        for row in player_rows:
            player_stats = \
                map(lambda x:
                    unicode('0') if x == '-' else x, [x.text for x in row])
            if any(map(lambda x: x in player_stats[0], NFL_FAN_POSITIONS)):
                pos = filter(lambda x:
                             x in player_stats[0], NFL_FAN_POSITIONS)[0]
                name = player_stats[0].split(pos)[0].rstrip()
                projected_points = calculate_ppr(pos, player_stats)
                if projected_points != 0:
                    hold.append([name, projected_points])
    for i in (0, 25):
        r = requests.get(NFL_FAN_URL.format(i, '8'))
        soup = BS(r.text, 'html.parser')
        player_rows = filter(lambda x: x,
                             [x.find_all('td') for x in soup.find_all('tr')])
        for row in player_rows:
            player_stats = \
                map(lambda x:
                    unicode('0') if x == '-' else x, [x.text for x in row])
            if any(map(lambda x: x in player_stats[0], ['DEF'])):
                name = player_stats[0].split('DEF')[0].rstrip()
                projected_points = calculate_ppr('DEF', player_stats)
                hold.append([name, projected_points])
    return hold


def calculate_ppr(pos, row):
    projected_points = 0
    if pos != 'DEF':
        projected_points += \
            (0.04 * float(row[2])) + \
            (4 * float(row[3])) + \
            (-1 * float(row[4])) + \
            (3 if float(row[2]) >= 300 else 0) + \
            (0.1 * float(row[5])) + \
            (6 * float(row[6])) + \
            (3 if float(row[5]) >= 100 else 0) + \
            (0.1 * float(row[7])) + \
            (3 if float(row[7]) >= 100 else 0) + \
            (6 * float(row[8])) + \
            (6 * float(row[9])) + \
            (2 * float(row[10])) + \
            (-1 * float(row[11]))
    if pos == 'DEF':
        projected_points += \
            (1 * float(row[2])) + \
            (2 * float(row[3])) + \
            (2 * float(row[4])) + \
            (2 * float(row[5])) + \
            (6 * float(row[6])) + \
            (2 * float(row[7])) + \
            (6 * float(row[8]))
        points_allowed = float(row[9])
        if points_allowed == 0:
            projected_points += 10
        elif points_allowed <= 6:
            projected_points += 7
        elif points_allowed <= 13:
            projected_points += 4
        elif points_allowed <= 20:
            projected_points += 1
        elif points_allowed <= 27:
            pass
        elif points_allowed <= 34:
            projected_points += -1
        else:
            projected_points += -4
    return round(projected_points, 2)


def write_to_csv(hold, file_path):
    with open(file_path, 'w') as fp:
        w = csv.writer(fp, delimiter=',')
        w.writerows(hold)
