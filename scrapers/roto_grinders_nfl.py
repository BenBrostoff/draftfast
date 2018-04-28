import csv

import requests

from nfl.data_cleaning_constants import DUPLICATES, RENAMES

ROTO_GRINDERS = ''.join([
    'https://rotogrinders.com',
    '/projected-stats/nfl-{}.csv?site=draftkings'
])

pos = ['qb', 'rb', 'wr', 'te', 'defense']


def scrape(cmd_args, use='avg'):
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
                if p[0] in RENAMES:
                    dk_name = RENAMES[p[0]]
                    print(
                        'Renaming {} to {} to match DraftKings'
                        .format(p[0], dk_name)
                    )
                    p[0] = dk_name

                # fragile - will break if RG changes their CSV
                proj = p[-1]
                if use == 'max':
                    proj = p[-3]
                elif use == 'min':
                    proj = p[-2]

                hold.append([p[0], proj or p[-1]])

    with open(cmd_args.projection_file, 'w') as fp:
        w = csv.writer(fp, delimiter=',')
        w.writerows(hold)
