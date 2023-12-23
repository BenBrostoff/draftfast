import csv
from itertools import islice
from draftfast.pickem import pickem_orm


def map_pids(pid_file):
    player_map = {}
    with open(pid_file, "r") as f:
        n = 0
        fields = None
        for line in f.readlines():
            n += 1
            if "TeamAbbrev" in line:  # line with field names was found
                fields = line.split(",")
                break

        f.close()
        f = islice(open(pid_file, "r"), n, None)
        reader = csv.DictReader(f, fieldnames=fields)
        for line in reader:
            player_map[line["Name"]] = line["ID"]

    return player_map


def write_to_csv(player_map, roster, writer):
    row = {
        pickem_orm.T1: player_map[roster.T1.name],
        pickem_orm.T2: player_map[roster.T2.name],
        pickem_orm.T3: player_map[roster.T3.name],
        pickem_orm.T4: player_map[roster.T4.name],
        pickem_orm.T5: player_map[roster.T5.name],
        pickem_orm.T6: player_map[roster.T6.name],
    }
    writer.writerow(row)
