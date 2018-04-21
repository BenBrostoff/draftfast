import csv
import requests

ROTO_GRINDERS = ''.join([
    'https://rotogrinders.com',
    '/projected-stats/mlb-{}.csv?site=draftkings'
])


def scrape():
    hold = [['playername', 'points']]
    for pos in ['hitter', 'pitcher']:
        content = requests.get(
            ROTO_GRINDERS.format(pos)
        ).content.decode('utf-8')
        cr = csv.reader(content.splitlines(), delimiter=',')
        for p in list(cr):
            if len(p):
                hold.append([p[0], p[-1]])

    with open('data/current-projections.csv', 'w') as fp:
        w = csv.writer(fp, delimiter=',')
        w.writerows(hold)
