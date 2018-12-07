import os
import csv
from itertools import islice
from draftfast.rules import DRAFT_KINGS, FAN_DUEL
from draftfast import dke_exceptions as dke

upload_file = '{}/data/current-upload.csv'.format(os.getcwd())

NAME_MAP = {
    DRAFT_KINGS: {
        'start': 'TeamAbbrev',
        'name': 'Name',
        'position': 'Position',
        'id': 'ID',
    },
    FAN_DUEL: {
        'start': '"Nickname"',
        'name': '"Nickname"',
        'position': '"Position"',
        'id': '"Player ID + Player Name"',
    },
}


def map_pids(pid_file, game=DRAFT_KINGS):
    start = NAME_MAP.get(game).get('start')
    name = NAME_MAP.get(game).get('name')
    position = NAME_MAP.get(game).get('position')
    p_id = NAME_MAP.get(game).get('id')

    player_map = {}
    with open(pid_file, 'r') as f:
        n = 0
        fields = None
        for line in f.readlines():
            n += 1
            if start in line:  # line with field names was found
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
            player_map[line[name] + " " + line[position]] = line[p_id]

    return player_map


def write_to_csv(writer, player_map, roster, game=DRAFT_KINGS):
    players = roster.sorted_players()

    ordered_possible = []
    if game == DRAFT_KINGS:
        ordered_possible = [
            _on_position(players, ['PG']),
            _on_position(players, ['SG']),
            _on_position(players, ['SF']),
            _on_position(players, ['PF']),
            _on_position(players, ['C']),
            _on_position(players, ['SG', 'PG']),
            _on_position(players, ['SF', 'PF']),
            players
        ]
    elif game == FAN_DUEL:
        ordered_possible = [
            _on_position(players, ['PG']),
            _on_position(players, ['PG']),
            _on_position(players, ['SG']),
            _on_position(players, ['SG']),
            _on_position(players, ['SF']),
            _on_position(players, ['SF']),
            _on_position(players, ['PF']),
            _on_position(players, ['PF']),
            _on_position(players, ['C']),
        ]

    ordered_lineup = []
    counter = 0
    for ps in ordered_possible:
        counter += 1
        not_used_ps = [
            p for p in ps
            if p not in ordered_lineup
        ]
        ordered_lineup.append(not_used_ps[0])

    writer.writerow([
        p.get_player_id(player_map)
        for p in ordered_lineup
    ])


def _on_position(players, possible):
    return [p for p in players if p.pos in possible]
