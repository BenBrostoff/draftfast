import re
import csv
import requests
from bs4 import BeautifulSoup as BS
import unicodedata

from ppr import calculate_fanpros_ppr
from constants import ALL_POS, ALL_NFL_TEAMS

ALL_NFL_TEAMS.extend(('GB', 'JAC', 'LA'))

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



def scrape():
    hold = []
    hold.append(['playername', 'points'])
    for page in build_fp_pages():
        r = requests.get(page[0])
        soup = BS(r.text, 'html.parser')
        for row in soup.find_all('tr', class_=re.compile('mpb-player-')):
            try:
                player_row = row.find_all('td')
                name = str(player_row[0].text)
                for team in ALL_NFL_TEAMS:
                    name = name.replace(team, '')
                hold.append([
                    name.rstrip(),
                    calculate_fanpros_ppr(player_row, page[1])
                ])
            except Exception, e:
                print 'Error scraping FanPros data: {}'.format(e)

    with open('data/current-fan-pros-projections.csv', 'w') as fp:
        w = csv.writer(fp, delimiter=',')
        w.writerows(hold)
