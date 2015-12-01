from sys import argv
import csv
import requests
from bs4 import BeautifulSoup as BS
import unicodedata

from constants import FFPRO

def build_fp_pages(use_espn=1):
    '''
    Scrape FanPros - for some reason, defense projections disappear mid-week
    so option exists to just scrape ESPN here
    '''
    fp_pages = []
    pos = ['qb', 'rb', 'wr', 'te', 'k', 'dst']
    if use_espn:
        pos.remove('dst')
        fp_pages.append('http://games.espn.go.com/ffl/tools/projections?slotCategoryId=16')
    for page in pos:
        fp_pages.append(
            FFPRO + '{0}.php?week={1}'.format(page, argv[1])
        )

    return fp_pages

def unicode_normalize(*args):
    defense = []
    for x in args:
        defense.append(unicodedata.normalize('NFKD', x).encode('ascii','ignore'))
    return defense

def scrape():
    hold = []
    hold.append(['playername', 'points'])
    for page in build_fp_pages():
        r = requests.get(page)
        soup = BS(r.text, 'html.parser')
        if 'espn' in page:
            for row in soup.select('.playerTableTable tr'):
                try:
                    p_check = row.findAll(class_="playertablePlayerName")
                    if len(p_check) == 0:
                        continue
                    defense_name = p_check[0].text
                    defense_points = row.find_all('td')[-1].text
                    defense = unicode_normalize(defense_name, defense_points)
                    hold.append(defense)
                except Exception, e:
                    print 'Error scraping ESPN data: ' + str(e)


        else:
            for row in soup.select('tr.mpb-available'):
                try:
                    hold.append([str(row.find_all('td')[0].text),
                                 str(row.find_all('td')[-1].text)])
                    
                except Exception, e:
                    print 'Error scraping FanPros data: ' + str(e)

    with open('data/fan-pros.csv', 'w') as fp:
        w = csv.writer(fp, delimiter=',')
        w.writerows(hold)

if __name__ == "__main__":
    scrape()
