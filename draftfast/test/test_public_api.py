import os
from nose import tools as ntools
from draftfast.optimize import run
from draftfast import rules
from draftfast.orm import Player
from draftfast.csv_parse import salary_download
from draftfast.settings import OptimizerSettings, PlayerPoolSettings

mock_player_pool = [
    Player(name='A1', cost=5500, proj=55, pos='PG'),
    Player(name='A2', cost=5500, proj=55, pos='PG'),
    Player(name='A3', cost=5500, proj=55, pos='SG'),
    Player(name='A4', cost=5500, proj=55, pos='SG'),
    Player(name='A5', cost=5500, proj=55, pos='SF'),
    Player(name='A6', cost=5500, proj=55, pos='SF'),
    Player(name='A7', cost=5500, proj=55, pos='PF'),
    Player(name='A8', cost=5500, proj=55, pos='PF'),
    Player(name='A9', cost=5500, proj=55, pos='C'),
    Player(name='A10', cost=5500, proj=55, pos='C'),
]

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
salary_file = '{}/data/test-salaries.csv'.format(CURRENT_DIR)
fd_nfl_salary_file = '{}/data/fd-nfl-salaries.csv'.format(CURRENT_DIR)
projection_file = '{}/data/test-projections.csv'.format(CURRENT_DIR)


def test_nba_dk():
    roster = run(
        rule_set=rules.DK_NBA_RULE_SET,
        player_pool=mock_player_pool,
        verbose=True,
    )
    ntools.assert_not_equals(roster, None)


def test_nba_dk_with_csv():
    roster = run(
        rule_set=rules.DK_NBA_RULE_SET,
        player_pool=mock_player_pool,
        verbose=True,
    )
    ntools.assert_not_equals(roster, None)


def test_nba_fd():
    roster = run(
        rule_set=rules.FD_NBA_RULE_SET,
        player_pool=mock_player_pool,
    )
    ntools.assert_not_equals(roster, None)


def test_nfl_dk():
    players = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        projection_file_location=projection_file,
        game=rules.DRAFT_KINGS,
    )
    roster = run(
        rule_set=rules.DK_NFL_RULE_SET,
        player_pool=players,
    )
    ntools.assert_not_equals(roster, None)


def test_nfl_fd():
    players = salary_download.generate_players_from_csvs(
        salary_file_location=fd_nfl_salary_file,
        game=rules.FAN_DUEL,
    )
    roster = run(
        rule_set=rules.FD_NFL_RULE_SET,
        player_pool=players,
    )
    ntools.assert_not_equals(roster, None)


def test_multi_roster():
    players = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        projection_file_location=projection_file,
        game=rules.DRAFT_KINGS,
    )
    roster = run(
        rule_set=rules.DK_NFL_RULE_SET,
        player_pool=players,
    )
    second_roster = run(
        rule_set=rules.DK_NFL_RULE_SET,
        player_pool=players,
        optimizer_settings=OptimizerSettings(
            existing_rosters=[roster],
        ),
    )

    ntools.assert_not_equals(roster, None)
    ntools.assert_not_equals(second_roster, None)
    ntools.assert_not_equals(roster == second_roster, True)


def test_stack():
    players = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        projection_file_location=projection_file,
        game=rules.DRAFT_KINGS,
    )
    roster = run(
        rule_set=rules.DK_NFL_RULE_SET,
        player_pool=players,
        optimizer_settings=OptimizerSettings(
            stack_team='NE',
            stack_count=5,
        )
    )
    ne_players_count = len([
        p for p in roster.sorted_players()
        if p.team == 'NE'
    ])
    ntools.assert_equals(5, ne_players_count)


def test_force_combo():
    # no combo
    players = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        projection_file_location=projection_file,
        game=rules.DRAFT_KINGS,
    )
    roster = run(
        rule_set=rules.DK_NFL_RULE_SET,
        player_pool=players,
        optimizer_settings=OptimizerSettings(
            stack_team='NE',
            stack_count=5,
        )
    )
    qb = roster.sorted_players()[0]
    team_count = len([
        x for x in roster.sorted_players()
        if x.team == qb.team
    ])
    ntools.assert_equals(team_count, 1)

    # QB/WR combo
    players = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        projection_file_location=projection_file,
        game=rules.DRAFT_KINGS,
    )
    roster = run(
        rule_set=rules.DK_NFL_RULE_SET,
        player_pool=players,
        optimizer_settings=OptimizerSettings(
            force_combo=True,
        )
    )
    qb = roster.sorted_players()[0]
    ntools.assert_equal(qb.pos, 'QB')

    # TODO - FIX
    # team_count = len([
    #     x for x in roster.sorted_players()
    #     if x.team == qb.team
    # ])
    # ntools.assert_equals(team_count, 2)


def test_te_combo():
    players = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        projection_file_location=projection_file,
        game=rules.DRAFT_KINGS,
    )
    roster = run(
        rule_set=rules.DK_NFL_RULE_SET,
        player_pool=players,
        optimizer_settings=OptimizerSettings(
            force_combo=True,
            combo_allow_te=True,
        )
    )
    qb = roster.sorted_players()[0]
    ntools.assert_equal(qb.pos, 'QB')
    team_count = len([
        x for x in roster.sorted_players()
        if x.team == qb.team and x.pos == 'TE'
    ])
    ntools.assert_equals(team_count, 1)


def test_no_double_te():
    players = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        projection_file_location=projection_file,
        game=rules.DRAFT_KINGS,
    )
    roster = run(
        rule_set=rules.DK_NFL_RULE_SET,
        player_pool=players,
        player_settings=PlayerPoolSettings(
            locked=['Rob Gronkowski']
        )
    )
    qb = roster.sorted_players()[0]
    ntools.assert_equal(qb.pos, 'QB')

    # TODO - FIX
    # te_count = len([
    #     x for x in roster.sorted_players()
    #     if x.pos == 'TE'
    # ])
    # ntools.assert_equals(te_count, 2)
    #
    # roster = run(
    #     rule_set=rules.DK_NFL_RULE_SET,
    #     player_pool=players,
    #     player_settings=PlayerPoolSettings(
    #         locked=['Rob Gronkowski'],
    #     )
    # )
    # qb = roster.sorted_players()[0]
    # ntools.assert_equal(qb.pos, 'QB')

    # te_count = len([
    #     x for x in roster.sorted_players()
    #     if x.pos == 'TE'
    # ])
    # ntools.assert_equals(te_count, 1)
