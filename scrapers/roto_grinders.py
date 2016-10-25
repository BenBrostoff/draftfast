import csv
import requests
from os import path

from data_cleaning_constants import DUPLICATES


CSV_FILE_PATH = path.join(
    path.split(path.split(path.realpath(__file__))[0])[0],
    'data',
    '{}'
)


ROTO_GRINDERS = ''.join([
    'https://rotogrinders.com',
    '/projected-stats/nfl-{}.csv?site=draftkings'
])


pos = ['qb', 'rb', 'wr', 'te', 'defense']


def scrape(file_name='current-projections.csv'):
    hold = [['playername', 'points']]
    for page in pos:
        content = requests.get(
            ROTO_GRINDERS.format(page)).content.decode('utf-8')
        cr = csv.reader(content.splitlines(), delimiter=',')
        for p in list(cr):
            if p[0] in [x['name'] for x in DUPLICATES]:
                entry = [x for x in DUPLICATES if
                         x['name'] == p[0]][0]
                if p[2].lower() != entry['team'].lower():
                    print "Skipping non-key duplicate %s" % p[0]
                    continue

            if len(p):
                hold.append([p[0], p[-1]])

    with open(CSV_FILE_PATH.format(file_name), 'w') as fp:
        w = csv.writer(fp, delimiter=',')
        w.writerows(hold)
