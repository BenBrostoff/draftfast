import os
from copy import deepcopy
from nose import tools as ntools
from draftfast.optimize import run
from draftfast import rules
from draftfast.orm import Player
from draftfast.csv_parse import salary_download
from draftfast.settings import OptimizerSettings, Stack
from draftfast.lineup_constraints import LineupConstraints

mock_nba_pool = [
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

mock_nfl_pool = [
    Player(name='A1', cost=5500, proj=40, pos='QB'),
    Player(name='A2', cost=5500, proj=41, pos='QB'),
    Player(name='A11', cost=5500, proj=50, pos='WR'),
    Player(name='A3', cost=5500, proj=42, pos='WR'),
    Player(name='A4', cost=5500, proj=43, pos='WR'),
    Player(name='A5', cost=5500, proj=44, pos='WR'),
    Player(name='A6', cost=5500, proj=45, pos='RB'),
    Player(name='A7', cost=5500, proj=46, pos='RB'),
    Player(name='A8', cost=5500, proj=47, pos='RB'),
    Player(name='A9', cost=5500, proj=48, pos='TE'),
    Player(name='A10', cost=5500, proj=49, pos='TE'),
    Player(name='A12', cost=5500, proj=51, pos='DST'),
    Player(name='A13', cost=5500, proj=52, pos='DST'),
]


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
salary_file = '{}/data/dk-nfl-salaries.csv'.format(CURRENT_DIR)
fd_nfl_salary_file = '{}/data/fd-nfl-salaries.csv'.format(CURRENT_DIR)
projection_file = '{}/data/dk-nfl-projections.csv'.format(CURRENT_DIR)


def test_nba_dk():
    roster = run(
        rule_set=rules.DK_NBA_RULE_SET,
        player_pool=mock_nba_pool,
        verbose=True,
    )
    ntools.assert_not_equal(roster, None)


def test_nba_dk_with_csv():
    roster = run(
        rule_set=rules.DK_NBA_RULE_SET,
        player_pool=mock_nba_pool,
        verbose=True,
    )
    ntools.assert_not_equal(roster, None)


def test_nba_fd():
    roster = run(
        rule_set=rules.FD_NBA_RULE_SET,
        player_pool=mock_nba_pool,
        verbose=True
    )
    ntools.assert_not_equal(roster, None)


def test_nfl_dk_mock():
    roster = run(
        rule_set=rules.DK_NFL_RULE_SET,
        player_pool=mock_nfl_pool,
    )

    ntools.assert_not_equal(roster, None)
    ntools.assert_equal(roster.projected(), 420.0)


def test_nfl_dk():
    players = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        projection_file_location=projection_file,
        game=rules.DRAFT_KINGS,

    )
    roster = run(
        rule_set=rules.DK_NFL_RULE_SET,
        player_pool=players,
        verbose=True
    )

    ntools.assert_not_equal(roster, None)
    ntools.assert_equal(roster.projected(), 124.30)


def test_nfl_fd():
    players = salary_download.generate_players_from_csvs(
        salary_file_location=fd_nfl_salary_file,
        game=rules.FAN_DUEL,
    )
    roster = run(
        rule_set=rules.FD_NFL_RULE_SET,
        player_pool=players,
        verbose=True
    )

    ntools.assert_not_equal(roster, None)
    ntools.assert_equal(roster.projected(), 155.0172712846236)


def test_multi_position():
    players = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        projection_file_location=projection_file,
        game=rules.DRAFT_KINGS,
    )
    roster = run(
        rule_set=rules.DK_NFL_RULE_SET,
        player_pool=players,
        constraints=LineupConstraints(
            locked=['Eli Manning'],
        ),
        verbose=True
    )
    ntools.assert_not_equal(roster, None)
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
        verbose=True
    )
    second_roster = run(
        rule_set=rules.DK_NFL_RULE_SET,
        player_pool=players,
        optimizer_settings=OptimizerSettings(
            existing_rosters=[roster],
        ),
        verbose=True
    )

    ntools.assert_not_equal(roster, None)
    ntools.assert_not_equal(second_roster, None)
    ntools.assert_false(roster.exact_equal(second_roster))


def test_multi_roster_nba():
    roster = run(
        rule_set=rules.DK_NBA_RULE_SET,
        player_pool=mock_nba_pool,
    )
    second_roster = run(
        rule_set=rules.DK_NBA_RULE_SET,
        player_pool=mock_nba_pool,
        optimizer_settings=OptimizerSettings(
            existing_rosters=[roster],
        ),
    )

    ntools.assert_not_equal(roster, None)
    ntools.assert_not_equal(second_roster, None)
    ntools.assert_false(roster.exact_equal(second_roster))


def test_uniques_nba():
    roster = run(
        rule_set=rules.DK_NBA_RULE_SET,
        player_pool=mock_nba_pool,
    )
    second_roster = run(
        rule_set=rules.DK_NBA_RULE_SET,
        player_pool=mock_nba_pool,
        optimizer_settings=OptimizerSettings(
            existing_rosters=[roster],
        ),
    )
    third_roster = run(
        rule_set=rules.DK_NBA_RULE_SET,
        player_pool=mock_nba_pool,
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


def test_respect_lock():
    players = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        projection_file_location=projection_file,
        game=rules.DRAFT_KINGS,
    )

    roster = run(
        rule_set=rules.DK_NFL_RULE_SET,
        player_pool=players,
        verbose=True,
        constraints=LineupConstraints(
            locked=['Andrew Luck'],
        ),
    )
    qb = roster.sorted_players()[0]
    ntools.assert_equal(qb.pos, 'QB')
    ntools.assert_equal(qb.name, 'Andrew Luck')


def test_respect_ban():
    players = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        projection_file_location=projection_file,
        game=rules.DRAFT_KINGS,
    )

    roster = run(
        rule_set=rules.DK_NFL_RULE_SET,
        player_pool=players,
        verbose=True,
        constraints=LineupConstraints(
            banned=['Eli Manning'],
        ),
    )
    for player in roster.sorted_players():
        ntools.assert_not_equal(player.name, 'Eli Manning')


def test_respect_group1():
    players = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        projection_file_location=projection_file,
        game=rules.DRAFT_KINGS,
    )

    grouped_players = ('DeAndre Hopkins', 'Amari Cooper', 'Sammy Watkins')

    roster = run(
        rule_set=rules.DK_NFL_RULE_SET,
        player_pool=players,
        verbose=True,
        constraints=LineupConstraints(
            groups=[
                [grouped_players, 2]
            ],
        ),
    )

    group_count = len([
        x for x in roster.sorted_players() if x.name in grouped_players
    ])
    ntools.assert_equal(group_count, 2)


def test_respect_group2():
    players = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        projection_file_location=projection_file,
        game=rules.DRAFT_KINGS,
    )

    grouped_players = (
        'Ryan Fitzpatrick',
        'Lamar Miller',
        'DeAndre Hopkins',
        'Amari Cooper',
        'Sammy Watkins'
    )

    roster = run(
        rule_set=rules.DK_NFL_RULE_SET,
        player_pool=players,
        verbose=True,
        constraints=LineupConstraints(
            groups=[
                [grouped_players, (2, 3)]
            ],
        ),
    )

    group_count = len([
        x for x in roster.sorted_players() if x.name in grouped_players
    ])
    ntools.assert_true(group_count >= 2 and group_count <= 3)


def test_respect_group3():
    players = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        projection_file_location=projection_file,
        game=rules.DRAFT_KINGS,
    )

    grouped_players = (
        'Ryan Fitzpatrick',
        'Lamar Miller',
        'DeAndre Hopkins',
        'Amari Cooper',
        'Sammy Watkins'
    )

    roster = run(
        rule_set=rules.DK_NFL_RULE_SET,
        player_pool=players,
        verbose=True,
        constraints=LineupConstraints(
            groups=[
                [grouped_players, 1]
            ],
        ),
    )

    group_count = len([
        x for x in roster.sorted_players() if x.name in grouped_players
    ])
    ntools.assert_true(group_count == 1)


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
            stacks=[
                Stack(team='NE', count=5)
            ]
        ),
        verbose=True,
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
            stacks=[
                Stack(team='NE', count=5)
            ]
        ),
        constraints=LineupConstraints(
            locked=['Sam Bradford'],
        ),
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
        ),
        constraints=LineupConstraints(
            banned=['Ryan Fitzpatrick']
        ),
        verbose=True,
    )
    qb = roster.sorted_players()[0]
    ntools.assert_equal(qb.pos, 'QB')

    wr_team_count = len([
        x for x in roster.sorted_players()
        if x.team == qb.team and x.pos == 'WR'
    ])
    ntools.assert_equals(wr_team_count, 1)

    te_team_count = len([
        x for x in roster.sorted_players()
        if x.team == qb.team and x.pos == 'TE'
    ])
    ntools.assert_equals(te_team_count, 0)


def test_te_combo():
    # use lock and ban to make a non-globally optimal QB/TE combo optimal
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
        ),
        constraints=LineupConstraints(
            banned=['Kellen Davis'],
            locked=['Philip Rivers'],
        ),
        verbose=True,
    )
    qb = roster.sorted_players()[0]
    ntools.assert_equal(qb.pos, 'QB')
    team_count = len([
        x for x in roster.sorted_players()
        if x.team == qb.team and x.pos == 'TE'
    ])
    ntools.assert_equals(team_count, 1)

    # make sure WR/QB still works
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
        ),
        constraints=LineupConstraints(
            locked=['Andrew Luck'],
        ),
        verbose=True,
    )
    qb = roster.sorted_players()[0]
    ntools.assert_equal(qb.pos, 'QB')
    team_count = len([
        x for x in roster.sorted_players()
        if x.team == qb.team and x.pos == 'WR'
    ])
    ntools.assert_equals(team_count, 1)

# def test_no_double_te():
#     # check double TE allowed
#     players = salary_download.generate_players_from_csvs(
#         salary_file_location=salary_file,
#         projection_file_location=projection_file,
#         game=rules.DRAFT_KINGS,
#     )
#     roster = run(
#         rule_set=rules.DK_NFL_RULE_SET,
#         player_pool=players,
#         verbose=True,
#         constraints=LineupConstraints(
#             locked=['Rob Gronkowski']
#         ),
#     )
#     qb = roster.sorted_players()[0]
#     ntools.assert_equal(qb.pos, 'QB')

#     te_count = len([
#         x for x in roster.sorted_players()
#         if x.pos == 'TE'
#     ])
#     ntools.assert_equals(te_count, 2)

#     # ban double te
#     roster = run(
#         rule_set=rules.DK_NFL_RULE_SET,
#         player_pool=players,
#         constraints=LineupConstraints(
#             locked=['Rob Gronkowski'],
#         )
#     )
#     qb = roster.sorted_players()[0]
#     ntools.assert_equal(qb.pos, 'QB')

#     te_count = len([
#         x for x in roster.sorted_players()
#         if x.pos == 'TE'
#     ])
#     ntools.assert_equals(te_count, 1)


def test_impossible_constraints():
    players = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        projection_file_location=projection_file,
        game=rules.DRAFT_KINGS,
    )
    roster = run(
        rule_set=rules.DK_NFL_RULE_SET,
        player_pool=players,
        optimizer_settings=OptimizerSettings(
            stacks=[
                Stack(team='NE', count=100)
            ],
            no_offense_against_defense=True
        ),
        constraints=LineupConstraints(
            banned=['Sammy Watkins', 'Kellen Davis'],
            locked=['Spencer Ware'],
            groups=[
                [('Philip Rivers', 'Sam Bradford', 'Andrew Luck'), 2],
                [('Saints', 'Alshon Jeffery', 'Lamar Miller'), (1, 3)]
            ]
        ),
        verbose=True
    )

    ntools.assert_equal(roster, None)


def test_multi_position_group_constraint():
    players = [
        Player(name='A', cost=5500, proj=400, pos='QB',
               possible_positions='QB/WR', multi_position=True),
        Player(name='A', cost=5500, proj=400, pos='WR',
               possible_positions='QB/WR', multi_position=True),
        Player(name='B', cost=5500, proj=41, pos='QB'),
        Player(name='C', cost=5500, proj=500, pos='WR',
               possible_positions='RB/WR', multi_position=True),
        Player(name='C', cost=5500, proj=500, pos='RB',
               possible_positions='RB/WR', multi_position=True),
        Player(name='D', cost=5500, proj=42, pos='WR'),
        Player(name='E', cost=5500, proj=43, pos='WR'),
        Player(name='F', cost=5500, proj=44, pos='WR'),
        Player(name='G', cost=5500, proj=45, pos='RB'),
        Player(name='H', cost=5500, proj=46, pos='RB'),
        Player(name='I', cost=5500, proj=47, pos='RB'),
        Player(name='J', cost=5500, proj=480, pos='TE',
               possible_positions='TE/WR', multi_position=True),
        Player(name='J', cost=5500, proj=480, pos='WR',
               possible_positions='TE/WR', multi_position=True),
        Player(name='K', cost=5500, proj=49, pos='TE'),
        Player(name='L', cost=5500, proj=51, pos='DST'),
        Player(name='M', cost=5500, proj=52, pos='DST'),
    ]

    grouped_players = ('A', 'C', 'J')

    roster = run(
        rule_set=rules.DK_NFL_RULE_SET,
        player_pool=players,
        constraints=LineupConstraints(
            groups=[
                [grouped_players, 2],
            ]
        ),
        verbose=True
    )

    group_count = len([
        x for x in roster.sorted_players() if x.name in grouped_players
    ])
    ntools.assert_equal(group_count, 2)
    ntools.assert_equal(roster.projected(), 1304)


def test_multi_position_group_constraint2():
    players = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        projection_file_location=projection_file,
        game=rules.DRAFT_KINGS,
    )

    grouped_players = ('Eli Manning', 'Dez Bryant', 'Geno Smith')

    roster = run(
        rule_set=rules.DK_NFL_RULE_SET,
        player_pool=players,
        constraints=LineupConstraints(
            groups=[
                [grouped_players, 2],
            ]
        ),
        verbose=True
    )

    group_count = len([
        x for x in roster.sorted_players() if x.name in grouped_players
    ])
    ntools.assert_equal(group_count, 2)
    ntools.assert_equal(roster.projected(), 120.89999999999999)


def test_no_opposing_def_dk_nfl_mock():
    mock_pool = [
        Player(name='A1', cost=5500, proj=40, pos='QB', team='X',
               matchup='X@Y'),
        Player(name='A2', cost=5500, proj=41, pos='QB', team='Y',
               matchup='X@Y'),
        Player(name='A11', cost=5500, proj=50, pos='WR', team='X',
               matchup='X@Y'),
        Player(name='A3', cost=5500, proj=42, pos='WR', team='Y',
               matchup='X@Y'),
        Player(name='A4', cost=5500, proj=43, pos='WR', team='X',
               matchup='X@Y'),
        Player(name='A5', cost=5500, proj=44, pos='WR', team='Y',
               matchup='X@Y'),
        Player(name='A111', cost=5500, proj=50, pos='WR', team='X',
               matchup='X@Y'),
        Player(name='A31', cost=5500, proj=42, pos='WR', team='Y',
               matchup='X@Y'),
        Player(name='A41', cost=5500, proj=62, pos='WR', team='X',
               matchup='X@Y'),
        Player(name='A51', cost=5500, proj=63, pos='WR', team='Y',
               matchup='X@Y'),
        Player(name='A6', cost=5500, proj=45, pos='RB', team='X',
               matchup='X@Y'),
        Player(name='A7', cost=5500, proj=46, pos='RB', team='Y',
               matchup='X@Y'),
        Player(name='A8', cost=5500, proj=47, pos='RB', team='X',
               matchup='X@Y'),
        Player(name='A71', cost=5500, proj=46, pos='RB', team='Y',
               matchup='X@Y'),
        Player(name='A81', cost=5500, proj=47, pos='RB', team='X',
               matchup='X@Y'),
        Player(name='A711', cost=5500, proj=46, pos='RB', team='Y',
               matchup='X@Y'),
        Player(name='A9', cost=5500, proj=48, pos='TE', team='X',
               matchup='X@Y'),
        Player(name='A10', cost=5500, proj=49, pos='TE', team='Y',
               matchup='X@Y'),
        Player(name='A12', cost=5500, proj=51, pos='DST', team='X',
               matchup='X@Y'),
        Player(name='A13', cost=5500, proj=500, pos='DST', team='Y',
               matchup='X@Y'),
    ]

    # mock pool is constructed such that optimal lineup has qb opposing dst
    roster = run(
        rule_set=rules.DK_NFL_RULE_SET,
        player_pool=mock_pool,
        verbose=True
    )

    ntools.assert_equal(roster.projected(), 909)
    qb_team = roster.sorted_players()[0].team
    dst_team = roster.sorted_players()[-1].team
    ntools.assert_equal(qb_team, dst_team)

    # this will fail to produce a roster because we only have 2 teams (X and Y)
    roster = run(
        rule_set=rules.DK_NFL_RULE_SET,
        player_pool=mock_pool,
        optimizer_settings=OptimizerSettings(
            no_offense_against_defense=True
        ),
        verbose=True
    )

    ntools.assert_equal(roster, None)

    # relax min teams
    roster = run(
        rule_set=rules.DK_NFL_RULE_SET,
        player_pool=mock_pool,
        optimizer_settings=OptimizerSettings(
            min_teams=1,
            no_offense_against_defense=True,
        ),
        verbose=True
    )

    ntools.assert_equal(roster.projected(), 877)
    ntools.assert_equal(len(set([p.team for p in roster.players])), 1)

    # add a player from a third team, min 2 teams
    mock_pool.append(Player(
        name='B2', cost=5500, proj=70, pos='QB', team='Q', matchup='Q@Z'
    )
    )
    roster = run(
        rule_set=rules.DK_NFL_RULE_SET,
        player_pool=deepcopy(mock_pool),
        optimizer_settings=OptimizerSettings(
            no_offense_against_defense=True
        ),
        verbose=True
    )

    for p in roster.players:
        if p.pos in rules.DK_NFL_RULE_SET.offensive_positions:
            ntools.assert_not_equal(p.team, 'X')


def test_no_opposing_def_dk_nfl():
    players = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        projection_file_location=projection_file,
        game=rules.DRAFT_KINGS,
    )

    roster = run(
        rule_set=rules.DK_NFL_RULE_SET,
        player_pool=players,
        optimizer_settings=OptimizerSettings(
            no_offense_against_defense=True
        ),
        constraints=LineupConstraints(
            locked=['Bengals']
        ),
        verbose=True
    )

    for p in roster.players:
        if p.pos in rules.DK_NFL_RULE_SET.offensive_positions:
            ntools.assert_not_equal(p.team, 'CIN')

    # force impossible lineup
    roster = run(
        rule_set=rules.DK_NFL_RULE_SET,
        player_pool=players,
        optimizer_settings=OptimizerSettings(
            no_offense_against_defense=True
        ),
        constraints=LineupConstraints(
            locked=['Bengals', 'Ryan Fitzpatrick']
        ),
        verbose=True
    )

    ntools.assert_equal(roster, None)


def test_no_opposing_def_fd_nfl():
    players = salary_download.generate_players_from_csvs(
        salary_file_location=fd_nfl_salary_file,
        game=rules.FAN_DUEL,
    )
    roster = run(
        rule_set=rules.FD_NFL_RULE_SET,
        player_pool=players,
        optimizer_settings=OptimizerSettings(
            no_offense_against_defense=True
        ),
        constraints=LineupConstraints(
            locked=['Jacksonville Jaguars']
        ),
        verbose=True
    )

    ntools.assert_not_equal(roster, None)

    for p in roster.players:
        if p.pos in rules.DK_NFL_RULE_SET.offensive_positions:
            ntools.assert_not_equal(p.team, 'IND')

    # force impossible lineup
    roster = run(
        rule_set=rules.FD_NFL_RULE_SET,
        player_pool=players,
        optimizer_settings=OptimizerSettings(
            no_offense_against_defense=True
        ),
        constraints=LineupConstraints(
            locked=['Eric Ebron', 'Jacksonville Jaguars']
        ),
        verbose=True
    )

    ntools.assert_equal(roster, None)


def test_no_mutate_side_Effect():
    players = salary_download.generate_players_from_csvs(
        salary_file_location=fd_nfl_salary_file,
        game=rules.FAN_DUEL,
    )
    run(
        rule_set=rules.FD_NFL_RULE_SET,
        player_pool=players,
        optimizer_settings=OptimizerSettings(
            no_offense_against_defense=True
        ),
        constraints=LineupConstraints(
            locked=['Tom Brady']
        ),
        verbose=True
    )
    brady = next((p for p in players if p.name == 'Tom Brady'))
    ntools.assert_equal(brady.lock, False)
