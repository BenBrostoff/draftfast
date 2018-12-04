import os
from nose import tools as ntools
from draftfast.orm import Player
from draftfast.optimize import run
from draftfast import rules
from draftfast.csv_parse import salary_download as sd


def test_general_guard():
    pg = Player(name='A', cost=1, proj=1, pos='PG')
    ntools.assert_equal(pg.nba_general_position, 'G')
    sg = Player(name='A', cost=1, proj=1, pos='SG')
    ntools.assert_equal(sg.nba_general_position, 'G')


def test_general_forward():
    pg = Player(name='A', cost=1, proj=1, pos='SF')
    ntools.assert_equal(pg.nba_general_position, 'F')
    sg = Player(name='A', cost=1, proj=1, pos='PF')
    ntools.assert_equal(sg.nba_general_position, 'F')


def test_general_center():
    pg = Player(name='A', cost=1, proj=1, pos='C')
    ntools.assert_equal(pg.nba_general_position, 'C')


def test_optimize_with_general():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    players = sd.generate_players_from_csvs(
        game=rules.DRAFT_KINGS,
        salary_file_location='{}/data/dk-nba-salaries.csv'.format(current_dir)
    )
    roster = run(
        rule_set=rules.DK_NBA_RULE_SET,
        player_pool=players,
        verbose=False,
    )

    def get_player_count_at_pos(pos):
        return len([
            p for p in roster.players
            if p.nba_general_position == pos
        ])

    ntools.assert_equal(3, get_player_count_at_pos('G'))
    ntools.assert_equal(3, get_player_count_at_pos('F'))
    ntools.assert_equal(2, get_player_count_at_pos('C'))
