import os
import csv
from nose.tools import assert_equal
from draftfast.csv_parse import uploaders
from draftfast.orm import NBARoster, Player

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

players = [
    Player(name='Stephen Curry', cost=1, proj=1, pos='SG'),
    Player(name='John Wall', cost=1, proj=1, pos='PG'),
    Player(name='Klay Thompson', cost=1, proj=1, pos='SG'),
    Player(name='Kevin Durant', cost=1, proj=1, pos='SF'),
    Player(name='Tobias Harris', cost=1, proj=1, pos='PF'),
    Player(name='Robert Covington', cost=1, proj=1, pos='SF'),
    Player(name='Anthony Davis', cost=1, proj=1, pos='C'),
    Player(name='Paul George', cost=1, proj=1, pos='PF'),
]

p_map = {}
for idx, p in enumerate(players):
    p.possible_positions = p.pos
    p_map['{} {}'.format(p.name, p.pos)] = idx


def test_upload():
    upload_file = '{}/data/current-upload.csv'.format(CURRENT_DIR)
    roster = NBARoster()
    for p in players:
        roster.add_player(p)

    uploader = uploaders.DraftKingsNBAUploader(
        pid_file='{}/data/dk_nba_pids.csv'.format(CURRENT_DIR),
        upload_file=upload_file,
    )
    uploader.write_rosters([roster])

    row = None
    with open(upload_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for idx, row in enumerate(reader):
            if idx == 0:
                continue
    assert_equal(
        row,
        ['1', '0', '3', '4', '6', '2', '5', '7']
    )
