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
    def get_player_count_at_pos(roster, pos):
        return len([
            p for p in roster.players
            if p.nba_general_position == pos
        ])

    current_dir = os.path.dirname(os.path.abspath(__file__))
    players = sd.generate_players_from_csvs(
        game=rules.DRAFT_KINGS,
        salary_file_location='{}/data/dk-nba-salaries.csv'.format(current_dir)
    )

    rosters = []

    for _ in range(30):
        rosters.append(
            run(
                rule_set=rules.DK_NBA_RULE_SET,
                player_pool=players,
                verbose=True,
            )
        )

    # (Possibly) due to how ortools works,
    # same players are produced with different positions
    #
    # this does appear to be an ortools artifact. Since the lineup produced is
    # correct and optimal either way, i modified the test to account for all
    # possible constructions
    ntools.assert_equal(rosters[0].projected(), 279.53)

    for i in range(1, 30):
        print(i)

        ntools.assert_equal(rosters[i], rosters[0])

        ntools.assert_equal(rosters[i].projected(), 279.53)
        ntools.assert_true(get_player_count_at_pos(rosters[i], 'G') in [3, 4])
        ntools.assert_true(get_player_count_at_pos(rosters[i], 'F') in [3, 4])
        ntools.assert_true(get_player_count_at_pos(rosters[i], 'C') in [1, 2])
