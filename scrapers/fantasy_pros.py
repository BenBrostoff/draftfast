import re
import csv
import requests
from os import path
from bs4 import BeautifulSoup as BS
import unicodedata

from draft_kings_fun.ppr import calculate_ppr, generate_empty_stat_dict
from draft_kings_fun.constants import ALL_POS

CSV_FILE_PATH = path.join(
    path.split(path.split(path.realpath(__file__))[0])[0],
    'data',
    '{}'
)

FFPRO = 'http://www.fantasypros.com/nfl/projections/'


def build_fp_pages():
    fp_pages = []
    for pos in ALL_POS:
        fp_pages.append([
            '{}{}.php'.format(FFPRO, pos.lower()), pos
        ])
    return fp_pages


def unicode_normalize(*args):
    defense = []
    for x in args:
        defense.append(unicodedata.normalize(
            'NFKD', x).encode('ascii', 'ignore'))
    return defense


def scrape(file_name='current-projections.csv'):
    hold = []
    hold.append(['playername', 'points'])
    for page in build_fp_pages():
        r = requests.get(page[0])
        soup = BS(r.text, 'html.parser')
        for row in soup.find_all('tr', class_=re.compile('mpb-player-')):
            try:
                player_row = row.find_all('td')
                hold.append([
                    str(player_row[0].text),
                    calculate_ppr(
                        page[1],
                        convert_fanpros_data(page[1],
                                             [x.text for x in player_row]))
                ])
            except Exception, e:
                print 'Error scraping FanPros data: {}'.format(e)

    with open(CSV_FILE_PATH.format(file_name), 'w') as fp:
        w = csv.writer(fp, delimiter=',')
        w.writerows(hold)


def convert_fanpros_data(pos, row):
    stat_dict = generate_empty_stat_dict(pos)

    # Placing stats into dict
    if pos.upper() == 'QB':
        stat_dict['PASS-YD'] = float(row[3])
        stat_dict['PASS-TD'] = float(row[4])
        stat_dict['INT'] = float(row[5])
        stat_dict['RUSH-YD'] = float(row[7])
        stat_dict['RUSH-TD'] = float(row[8])
        stat_dict['FL'] = float(row[9])
    elif pos.upper() == 'RB' or pos.upper() == 'WR':
        stat_dict['RUSH-YD'] = float(row[2])
        stat_dict['RUSH-TD'] = float(row[3])
        stat_dict['REC'] = float(row[4])
        stat_dict['REC-YD'] = float(row[5])
        stat_dict['REC-TD'] = float(row[6])
        stat_dict['FL'] = float(row[7])
    elif pos.upper() == 'TE':
        stat_dict['REC'] = float(row[1])
        stat_dict['REC-YD'] = float(row[2])
        stat_dict['REC-TD'] = float(row[3])
        stat_dict['FL'] = float(row[4])
    elif pos.upper() == 'DST':
        stat_dict['SACK'] = float(row[1])
        stat_dict['INT'] = float(row[2])
        stat_dict['FR'] = float(row[3])
        stat_dict['TD'] = float(row[5])
        stat_dict['SAFETY'] = float(row[7])
        stat_dict['POINTS_ALLOWED'] = float(row[8])
    return stat_dict
