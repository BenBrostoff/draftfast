import csv
import requests
from nba.data_cleaning_constants import RENAMES


ROTO_GRINDERS = ''.join([
    'https://rotogrinders.com',
    '/projected-stats/nba-player.csv?site=draftkings'
])


def scrape():
    hold = [['playername', 'points']]
    content = requests.get(
        ROTO_GRINDERS
    ).content.decode('utf-8')
    cr = csv.reader(content.splitlines(), delimiter=',')
    for p in list(cr):
        renames = \
            [x['dk_name'] for x in RENAMES
             if p[0] == x['name']]
        if renames:
            p[0] = renames[0]

        if len(p):
            hold.append([p[0], p[-1]])

    with open('data/current-projections.csv', 'w') as fp:
        w = csv.writer(fp, delimiter=',')
        w.writerows(hold)
