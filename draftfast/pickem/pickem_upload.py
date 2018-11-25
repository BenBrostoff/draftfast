import csv
from pickem import pickem_orm
from itertools import islice

upload_file = 'data/current-upload.csv'


def create_upload_file():
    with open(upload_file, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=pickem_orm.TIERS)
        writer.writeheader()


def map_pids(pid_file):
    player_map = {}
    with open(pid_file, 'r') as f:
        n = 0
        fields = None
        for line in f.readlines():
            n += 1
            if 'TeamAbbrev' in line:  # line with field names was found
                fields = line.split(',')
                break

        f.close()
        f = islice(open(pid_file, 'r'), n, None)
        reader = csv.DictReader(f, fieldnames=fields)
        for line in reader:
            player_map[line['Name']] = line['ID']

    return player_map


def update_upload_csv(player_map, tiered_lineup):
    with open(upload_file, 'a') as f:
        writer = csv.DictWriter(f, fieldnames=pickem_orm.TIERS)
        writer.writerow(
            {
                pickem_orm.T1: player_map[tiered_lineup.T1.name],
                pickem_orm.T2: player_map[tiered_lineup.T2.name],
                pickem_orm.T3: player_map[tiered_lineup.T3.name],
                pickem_orm.T4: player_map[tiered_lineup.T4.name],
                pickem_orm.T5: player_map[tiered_lineup.T5.name],
                pickem_orm.T6: player_map[tiered_lineup.T6.name],
            }
        )
