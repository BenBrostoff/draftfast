from sys import argv
import csv
import requests
from bs4 import BeautifulSoup as BS

from constants import FFPRO

def build_fp_pages():
    fp_pages = []
    for page in ['qb', 'rb', 'wr', 'te', 'k', 'dst']:
        fp_pages.append(
            FFPRO + '{0}.php?week={1}'.format(page, argv[1])
        )
    return fp_pages

def scrape():
    hold = []
    hold.append(['playername', 'points'])
    for page in build_fp_pages():
        r = requests.get(page)
        soup = BS(r.text)
        for row in soup.find_all('tr'):
            try:
                hold.append([str(row.find_all('td')[0].text),
                             str(row.find_all('td')[-1].text)])
                
            except Exception, e:
                print e

    with open('data/fan-pros.csv', 'w') as fp:
        w = csv.writer(fp, delimiter=',')
        w.writerows(hold)

if __name__ == "__main__":
    scrape()
