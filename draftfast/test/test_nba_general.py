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
    def get_player_count_at_pos(pos):
        return len([
            p for p in roster.players
            if p.nba_general_position == pos
        ])

    current_dir = os.path.dirname(os.path.abspath(__file__))
    players = sd.generate_players_from_csvs(
        game=rules.DRAFT_KINGS,
        salary_file_location='{}/data/dk-nba-salaries.csv'.format(current_dir)
    )

    prev_roster = None
    for _ in range(100):
        roster = run(
            rule_set=rules.DK_NBA_RULE_SET,
            player_pool=players,
            verbose=True,
        )

        # (Possibly) due to how ortools works,
        # same players are produced with different positions
        #
        # this does appear to be an ortools artifact. Since the lineup produced is
        # correct and optimal either way, i modified the test to account for all
        # possible constructions
        if prev_roster:
            ntools.assert_equal(roster, prev_roster)

        prev_roster = roster

        ntools.assert_equal(roster.projected(), 279.53)
        ntools.assert_true(get_player_count_at_pos('G') in [3, 4])
        ntools.assert_true(get_player_count_at_pos('F') in [3, 4])
        ntools.assert_true(get_player_count_at_pos('C') in [1, 2])
