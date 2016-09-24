import re
import csv
import requests
from bs4 import BeautifulSoup as BS
import unicodedata

from ppr import calculate_fanpros_ppr
from constants import ALL_POS

FFPRO = 'http://www.fantasypros.com/nfl/projections/'

def build_fp_pages():
    fp_pages = []
    for pos in ALL_POS:
        fp_pages.append([
            '{}{}.php'.format(FFPRO, pos), pos
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
                hold.append([str(player_row[0].text), calculate_fanpros_ppr(player_row, page[1])])
            except Exception, e:
                print 'Error scraping FanPros data: {}'.format(e)

    with open('data/current-projections.csv', 'w') as fp:
        w = csv.writer(fp, delimiter=',')
        w.writerows(hold)
