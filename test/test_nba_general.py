import os
from orm import Player
from optimize import run
from argparse import Namespace


def test_general_guard():
    pg = Player(name='A', cost=1, proj=1, pos='PG')
    assert pg.nba_general_position == 'G'
    sg = Player(name='A', cost=1, proj=1, pos='SG')
    assert sg.nba_general_position == 'G'


def test_general_forward():
    pg = Player(name='A', cost=1, proj=1, pos='SF')
    assert pg.nba_general_position == 'F'
    sg = Player(name='A', cost=1, proj=1, pos='PF')
    assert sg.nba_general_position == 'F'


def test_general_center():
    pg = Player(name='A', cost=1, proj=1, pos='C')
    assert pg.nba_general_position == 'C'


def test_optimize_with_general():
    run_args = Namespace(
        dtype='wr',
        duo='n',
        i=1,
        season=2016,
        w=1,
        historical='n',
        l='NBA',
        limit='n',
        lp=0,
        no_double_te='n',
        mp=100,
        ms=10000,
        s='n',
        sp=3000,
        home=None,
        locked=None,
        teams=None,
        banned=None,
        po=0,
        po_location=None,
        v_avg=10000,
        source='nba_rotogrinders',
        salary_file=os.getcwd() + '/test/data/nba-test-salaries.csv',
        projection_file=os.getcwd() + '/test/data/nba-test-projections.csv',
    )
    roster = run('NBA', [], run_args)

    def get_player_count_at_pos(pos):
        return len([
            p for p in roster.players
            if p.nba_general_position == pos
        ])

    assert 4 == get_player_count_at_pos('G')
    assert 3 == get_player_count_at_pos('F')
    assert 1 == get_player_count_at_pos('C')
