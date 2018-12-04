import csv
from itertools import islice

from draftfast import dke_exceptions as dke
from draftfast.nfl.data_cleaning_constants import RENAMES

upload_file = 'data/current-upload.csv'


def create_upload_file():
    with open(upload_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(
            ['QB', 'RB', 'RB',
             'WR', 'WR', 'WR', 'TE', 'FLEX', 'DST'])


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

        if not fields:
            raise dke.InvalidCSVUploadFileException(
                "Check that you're using the DK CSV upload template, " +
                "which can be found at " +
                "https://www.draftkings.com/lineup/upload.")

        f.close()
        f = islice(open(pid_file, "r"), n, None)
        reader = csv.DictReader(f, fieldnames=fields)
        for line in reader:
            player_map[line['Name'] + " " + line['Position']] = line['ID']

    return player_map


def update_upload_csv(player_map, roster):
    players = roster.sorted_players()
    with open(upload_file, 'a') as f:
        writer = csv.writer(f)
        player_ids = []
        flex_id = -1
        rbs, wrs, tes = 0, 0, 0

        for p in players:
            # For the players in the roster, get their id.
            # they are sorted when they are printed out,
            # so the order is good, except for the flex player
            p.name = _convert_to_dk_name(p.name)
            p_id = player_map[p.name + " " + p.pos]

            #  keep track of the flex player and write them out after the TE
            if p.pos == 'QB':
                player_ids.append(p_id)
            if p.pos == 'WR':
                if wrs == 3:
                    flex_id = p_id
                    continue
                wrs += 1
                player_ids.append(p_id)
            elif p.pos == 'RB':
                if rbs == 2:
                    flex_id = p_id
                    continue
                rbs += 1
                player_ids.append(p_id)
            elif p.pos == 'TE':
                if tes == 1:
                    flex_id = p_id
                    continue
                tes += 1
                player_ids.append(p_id)
            elif p.pos == 'DST':
                player_ids.append(flex_id)
                player_ids.append(p_id)

        writer.writerow(player_ids)


def _convert_to_dk_name(name):
    if name in RENAMES:
        return RENAMES['name']
    return name
