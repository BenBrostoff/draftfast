import os
from nose import tools as ntools
from draftfast.optimize import run, run_multi
from draftfast import rules
from draftfast.orm import Player
from draftfast.csv_parse import salary_download
from draftfast.settings import OptimizerSettings, PlayerPoolSettings

mock_player_pool = [
    Player(name='A1', cost=5500, proj=40, pos='PG'),
    Player(name='A2', cost=5500, proj=41, pos='PG'),
    Player(name='A11', cost=5500, proj=50, pos='PG'),
    Player(name='A3', cost=5500, proj=42, pos='SG'),
    Player(name='A4', cost=5500, proj=43, pos='SG'),
    Player(name='A5', cost=5500, proj=44, pos='SF'),
    Player(name='A6', cost=5500, proj=45, pos='SF'),
    Player(name='A7', cost=5500, proj=46, pos='PF'),
    Player(name='A8', cost=5500, proj=47, pos='PF'),
    Player(name='A9', cost=5500, proj=48, pos='C'),
    Player(name='A10', cost=5500, proj=49, pos='C'),
]

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
salary_file = '{}/data/dk-nfl-salaries.csv'.format(CURRENT_DIR)
fd_nfl_salary_file = '{}/data/fd-nfl-salaries.csv'.format(CURRENT_DIR)
projection_file = '{}/data/dk-nfl-projections.csv'.format(CURRENT_DIR)


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


def test_multi_position():
    players = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        projection_file_location=projection_file,
        game=rules.DRAFT_KINGS,
    )
    roster = run(
        rule_set=rules.DK_NFL_RULE_SET,
        player_pool=players,
        player_settings=PlayerPoolSettings(
            locked=['Eli Manning'],
        ),
    )
    ntools.assert_not_equals(roster, None)
    multi_pos = [p for p in roster.players if p.name == 'Eli Manning']
    ntools.assert_equal(len(multi_pos), 1)
    ntools.assert_equal(multi_pos[0].pos, 'TE')


def test_multi_roster_nfl():
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


def test_multi_roster_nba():
    roster = run(
        rule_set=rules.DK_NBA_RULE_SET,
        player_pool=mock_player_pool,
    )
    second_roster = run(
        rule_set=rules.DK_NBA_RULE_SET,
        player_pool=mock_player_pool,
        optimizer_settings=OptimizerSettings(
            existing_rosters=[roster],
        ),
    )

    ntools.assert_not_equals(roster, None)
    ntools.assert_not_equals(second_roster, None)
    ntools.assert_not_equals(roster == second_roster, True)


def test_uniques_nba():
    roster = run(
        rule_set=rules.DK_NBA_RULE_SET,
        player_pool=mock_player_pool,
    )
    second_roster = run(
        rule_set=rules.DK_NBA_RULE_SET,
        player_pool=mock_player_pool,
        optimizer_settings=OptimizerSettings(
            existing_rosters=[roster],
        ),
    )
    third_roster = run(
        rule_set=rules.DK_NBA_RULE_SET,
        player_pool=mock_player_pool,
        optimizer_settings=OptimizerSettings(
            existing_rosters=[roster],
            uniques=2,
        ),
    )

    players = roster.sorted_players()
    second_players = second_roster.sorted_players()
    third_players = third_roster.sorted_players()
    crossover_a = list(set(players).intersection(second_players))
    crossover_b = list(set(players).intersection(third_players))
    ntools.assert_equal(
        len(crossover_a),
        rules.DK_NBA_RULE_SET.roster_size - 1
    )
    ntools.assert_equal(
        len(crossover_b),
        rules.DK_NBA_RULE_SET.roster_size - 2
    )


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
        player_settings=PlayerPoolSettings(
            locked=['Sam Bradford'],
        ),
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


def test_deterministic_exposure_limits():
    iterations = 2
    players = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        projection_file_location=projection_file,
        game=rules.DRAFT_KINGS,
    )
    rosters, exposure_diffs = run_multi(
        iterations=2,
        rule_set=rules.DK_NFL_RULE_SET,
        player_pool=players,
        exposure_bounds=[
            {'name': 'Andrew Luck', 'min': 0.5, 'max': 0.7},
            {'name': 'Alshon Jeffery', 'min': 1, 'max': 1},
        ]
    )
    ntools.assert_equal(len(rosters), iterations)
    ntools.assert_equal(len(exposure_diffs), 0)

    players = [p.name for p in rosters[0].players]
    ntools.assert_true('Andrew Luck' in players)
    ntools.assert_true('Alshon Jeffery' in players)

    players = [p.name for p in rosters[1].players]
    ntools.assert_true('Andrew Luck' not in players)
    ntools.assert_true('Alshon Jeffery' in players)


def test_random_exposure_limits():
    iterations = 10
    players = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        projection_file_location=projection_file,
        game=rules.DRAFT_KINGS,
    )
    rosters, exposure_diffs = run_multi(
        iterations=iterations,
        exposure_random_seed=42,
        rule_set=rules.DK_NFL_RULE_SET,
        player_pool=players,
    )
    ntools.assert_equal(len(rosters), iterations)
    ntools.assert_equal(len(exposure_diffs), 0)
