import csv
import re
import unicodedata

import requests
from bs4 import BeautifulSoup as BS

from nfl.ppr import calculate_ppr, generate_empty_stat_dict
from nfl.data_cleaning_constants import RENAMES

FFPRO = 'http://www.fantasypros.com/nfl/projections/'
ALL_POS = ('QB', 'RB', 'WR', 'TE', 'DST')


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


def scrape(game='draftkings'):
    hold = []
    hold.append(['playername', 'points'])
    for page in build_fp_pages():
        r = requests.get(page[0])
        soup = BS(r.text, 'html.parser')
        for row in soup.find_all('tr', class_=re.compile('mpb-player-')):
            try:
                player_row = row.find_all('td')
                player_name = str(player_row[0].text)
                if player_name:
                    if player_name in RENAMES:
                        dk_name = RENAMES[player_name]
                        print(
                            'Renaming {} to {} to match DraftKings'
                            .format(player_name, dk_name)
                        )
                        player_name = dk_name

                hold.append([
                    player_name,
                    calculate_ppr(
                        page[1],
                        convert_fanpros_data(page[1],
                                             [x.text for x in player_row]))
                ])
            except Exception, e:
                print 'Error scraping FanPros data: {}'.format(e)

    with open('data/current-projections.csv', 'w') as fp:
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
