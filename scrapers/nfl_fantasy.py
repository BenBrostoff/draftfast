import csv
import requests
from bs4 import BeautifulSoup as BS
from os import path

from ppr import calculate_ppr, generate_empty_stat_dict

DEFAULT_FILE_PATH = path.join(
    path.split(path.split(path.realpath(__file__))[0])[0],
    'data',
    '{}'
)

NFL_FAN_POSITIONS = ['QB', 'RB', 'WR', 'TE', 'DEF']

NFL_FAN_URL = \
    'http://fantasy.nfl.com/research/projections?offset={}&position={}'


def scrape(limit=1000, file_name='current-projections.csv'):
    hold = scrape_nfl_fan(limit)
    write_to_csv(hold, DEFAULT_FILE_PATH.format(file_name))


def scrape_nfl_fan(limit):
    hold = []
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
                projected_points = \
                    calculate_ppr(pos,
                                  convert_nfl_fantasy_data(pos, player_stats))
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
                projected_points = \
                    calculate_ppr('DEF',
                                  convert_nfl_fantasy_data('DEF',
                                                           player_stats))
                hold.append([name, projected_points])
    return hold


def convert_nfl_fantasy_data(pos, row):
    stat_dict = generate_empty_stat_dict(pos)

    # Placing stats into dict
    if pos != 'DEF':
        stat_dict['PASS-YD'] = float(row[2])
        stat_dict['PASS-TD'] = float(row[3])
        stat_dict['INT'] = float(row[4])
        stat_dict['RUSH-YD'] = float(row[5])
        stat_dict['RUSH-TD'] = float(row[6])
        stat_dict['REC-YD'] = float(row[7])
        stat_dict['REC-TD'] = float(row[8])
        stat_dict['MISC-TD'] = float(row[9])
        stat_dict['2PT'] = float(row[10])
        stat_dict['FL'] = float(row[11])
    if pos == 'DEF':
        stat_dict['SACK'] = float(row[2])
        stat_dict['INT'] = float(row[3])
        stat_dict['FR'] = float(row[4])
        stat_dict['TD'] = float(row[6])
        stat_dict['SAFETY'] = float(row[5])
        stat_dict['2PT'] = float(row[7])
        stat_dict['POINTS_ALLOWED'] = float(row[9])
    return stat_dict


def write_to_csv(hold, file_path):
    with open(file_path, 'w') as fp:
        w = csv.writer(fp, delimiter=',')
        w.writerows(hold)
