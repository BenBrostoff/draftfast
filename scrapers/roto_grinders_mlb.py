import csv
import requests


def scrape(cmd_args):
    roto_grinders = ''.join([
        'https://rotogrinders.com',
        '/projected-stats/mlb-{}.csv?site={}'
    ])

    hold = [['playername', 'points']]
    for pos in ['hitter', 'pitcher']:
        url = roto_grinders.format(pos, cmd_args.game)
        content = requests.get(url).content.decode('utf-8')
        cr = csv.reader(content.splitlines(), delimiter=',')
        for p in list(cr):
            if len(p):
                hold.append([p[0], p[-1]])

    with open(cmd_args.projection_file, 'w') as fp:
        w = csv.writer(fp, delimiter=',')
        w.writerows(hold)
