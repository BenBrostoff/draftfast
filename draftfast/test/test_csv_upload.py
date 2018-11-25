import os
import csv

from nose.tools import assert_equal
from draftfast.csv_parse import nba_upload
from draftfast.orm import NBARoster, Player

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

players = [
    Player(name='A', cost=1, proj=1, pos='SG'),
    Player(name='B', cost=1, proj=1, pos='PG'),
    Player(name='C', cost=1, proj=1, pos='SG'),
    Player(name='D', cost=1, proj=1, pos='SF'),
    Player(name='E', cost=1, proj=1, pos='PF'),
    Player(name='F', cost=1, proj=1, pos='SF'),
    Player(name='G', cost=1, proj=1, pos='C'),
    Player(name='H', cost=1, proj=1, pos='PF')
]

p_map = {}
for idx, p in enumerate(players):
    p.possible_positions = p.pos
    p_map['{} {}'.format(p.name, p.pos)] = idx


def test_upload():
    roster = NBARoster()
    for p in players:
        roster.add_player(p)

    nba_upload.create_upload_file()
    nba_upload.update_upload_csv(p_map, roster)
    upload = '{}/data/current-upload.csv'.format(CURRENT_DIR)
    with open(upload, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for idx, row in enumerate(reader):
            if idx == 0:
                continue
            assert_equal(
                row,
                ['1', '0', '3', '4', '6', '2', '5', '7']
            )
