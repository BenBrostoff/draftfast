from sys import argv
import re
import csv
import requests
from bs4 import BeautifulSoup as BS
import unicodedata

from constants import FFPRO


def build_fp_pages():
    fp_pages = []
    pos = ['qb', 'rb', 'wr', 'te', 'k', 'dst']
    for page in pos:
        fp_pages.append(
            FFPRO + '{0}.php?week={1}'.format(page, argv[1]))

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
        r = requests.get(page)
        soup = BS(r.text, 'html.parser')
        for row in soup.find_all('tr', class_=re.compile('mpb-player-')):
            try:
                hold.append([str(row.find_all('td')[0].text),
                             str(row.find_all('td')[-1].text)])

            except Exception, e:
                print 'Error scraping FanPros data: ' + str(e)

    with open('data/current-projections.csv', 'w') as fp:
        w = csv.writer(fp, delimiter=',')
        w.writerows(hold)

if __name__ == "__main__":
    scrape()
