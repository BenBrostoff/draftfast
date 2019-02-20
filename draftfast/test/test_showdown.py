from nose import tools as ntools
from draftfast.optimize import run
from draftfast import rules
from draftfast.orm import Player
from draftfast.settings import OptimizerSettings
from draftfast.showdown.orm import ShowdownPlayer
from draftfast.lineup_constraints import LineupConstraints


def _build_mock_player_pool():
    player_pool = [
        Player(name='A1', cost=5500, proj=100, pos='QB',
               team='X', matchup='X@Y'),
        Player(name='A2', cost=5500, proj=41, pos='QB',
               team='X', matchup='X@Y'),
        Player(name='A11', cost=5500, proj=50, pos='WR',
               team='X', matchup='X@Y'),
        Player(name='A3', cost=5500, proj=42, pos='WR',
               team='X', matchup='X@Y'),
        Player(name='A4', cost=5500, proj=43, pos='WR',
               team='X', matchup='X@Y'),
        Player(name='A5', cost=5500, proj=44, pos='WR',
               team='X', matchup='X@Y'),
        Player(name='A6', cost=5500, proj=45, pos='RB',
               team='X', matchup='X@Y'),
        Player(name='A7', cost=5500, proj=46, pos='RB',
               team='X', matchup='X@Y'),
        Player(name='A8', cost=5500, proj=47, pos='RB',
               team='X', matchup='X@Y'),
        Player(name='A9', cost=5500, proj=48, pos='TE',
               team='X', matchup='X@Y'),
        Player(name='A10', cost=5500, proj=49, pos='TE',
               team='X', matchup='X@Y'),
        Player(name='A12', cost=5500, proj=51, pos='DST',
               team='X', matchup='X@Y'),
        Player(name='A14', cost=5500, proj=40, pos='QB',
               team='Y', matchup='X@Y'),
        Player(name='A21', cost=5500, proj=41, pos='QB',
               team='Y', matchup='X@Y'),
        Player(name='A11', cost=5500, proj=50, pos='WR',
               team='Y', matchup='X@Y'),
        Player(name='A31', cost=5500, proj=42, pos='WR',
               team='Y', matchup='X@Y'),
        Player(name='A41', cost=5500, proj=43, pos='WR',
               team='Y', matchup='X@Y'),
        Player(name='A51', cost=5500, proj=54, pos='WR',
               team='Y', matchup='X@Y'),
        Player(name='A61', cost=5500, proj=45, pos='RB',
               team='Y', matchup='X@Y'),
        Player(name='A71', cost=5500, proj=56, pos='RB',
               team='Y', matchup='X@Y'),
        Player(name='A81', cost=5500, proj=47, pos='RB',
               team='Y', matchup='X@Y'),
        Player(name='A91', cost=5500, proj=48, pos='TE',
               team='Y', matchup='X@Y'),
        Player(name='A110', cost=5500, proj=49, pos='TE',
               team='Y', matchup='X@Y'),
        Player(name='A112', cost=5500, proj=60, pos='DST',
               team='Y', matchup='X@Y'),
    ]

    mock_dk_pool = [ShowdownPlayer(p) for p in player_pool] + \
                   [ShowdownPlayer(p, captain=True) for p in player_pool]

    return mock_dk_pool


def test_nfl_dk_showdown_mock():
    mock_dk_pool = _build_mock_player_pool()

    roster = run(
        rule_set=rules.DK_NFL_SHOWDOWN_RULE_SET,
        player_pool=mock_dk_pool,
        optimizer_settings=OptimizerSettings(
            showdown_teams=('X', 'Y'),
        ),
        verbose=True
    )

    ntools.assert_not_equal(roster, None)
    ntools.assert_equal(roster.projected(), 421)


def test_nfl_showdown_no_def_against_capt():
    mock_dk_pool = _build_mock_player_pool()

    roster = run(
        rule_set=rules.DK_NFL_SHOWDOWN_RULE_SET,
        player_pool=mock_dk_pool,
        optimizer_settings=OptimizerSettings(
            showdown_teams=('X', 'Y'),
            no_defense_against_captain=True,
        ),
        verbose=True
    )

    ntools.assert_not_equal(roster, None)
    ntools.assert_equal(roster.projected(), 408.0)
    for p in roster.players:
        ntools.assert_not_equal(p.name, 'A112')


def test_nfl_showdown_lock_general():
    mock_dk_pool = _build_mock_player_pool()

    roster = run(
        rule_set=rules.DK_NFL_SHOWDOWN_RULE_SET,
        player_pool=mock_dk_pool,
        optimizer_settings=OptimizerSettings(
            showdown_teams=('X', 'Y'),
            no_defense_against_captain=True,
        ),
        constraints=LineupConstraints(
            locked=['A14'],
        ),
        verbose=True
    )
    ntools.assert_not_equal(roster, None)
    ntools.assert_equal(roster.projected(), 399.0)
    ntools.assert_true('A14' in [x.name for x in roster.players])


def test_nfl_showdown_lock_captain():
    mock_dk_pool = _build_mock_player_pool()

    roster = run(
        rule_set=rules.DK_NFL_SHOWDOWN_RULE_SET,
        player_pool=mock_dk_pool,
        optimizer_settings=OptimizerSettings(
            showdown_teams=('X', 'Y'),
            no_defense_against_captain=True,
        ),
        constraints=LineupConstraints(
            position_locked=['A2 CPT X'],
        ),
        verbose=True
    )
    ntools.assert_not_equal(roster, None)
    ntools.assert_equal(roster.projected(), 370.5)
    cpt = [x for x in roster.players if x.pos == 'CPT'][0]
    ntools.assert_equal('A2', cpt.name)


def test_nfl_showdown_lock_flex():
    mock_dk_pool = _build_mock_player_pool()

    roster = run(
        rule_set=rules.DK_NFL_SHOWDOWN_RULE_SET,
        player_pool=mock_dk_pool,
        optimizer_settings=OptimizerSettings(
            showdown_teams=('X', 'Y'),
            no_defense_against_captain=True,
        ),
        constraints=LineupConstraints(
            position_locked=['A1 FLEX X'],
        ),
        verbose=True
    )
    ntools.assert_not_equal(roster, None)
    ntools.assert_equal(roster.projected(), 386.0)
    flex = [
        x for x in roster.players
        if x.pos == 'FLEX'
        and x.name == 'A1'
    ][0]
    ntools.assert_equal('A1', flex.name)


def test_nfl_showdown_ban_general():
    mock_dk_pool = _build_mock_player_pool()

    roster = run(
        rule_set=rules.DK_NFL_SHOWDOWN_RULE_SET,
        player_pool=mock_dk_pool,
        optimizer_settings=OptimizerSettings(
            showdown_teams=('X', 'Y'),
            no_defense_against_captain=True,
        ),
        constraints=LineupConstraints(
            banned=['A1'],
        ),
        verbose=True
    )
    ntools.assert_not_equal(roster, None)
    ntools.assert_equal(roster.projected(), 334.0)
    ntools.assert_true('A1' not in [x.name for x in roster.players])


def test_nfl_showdown_ban_specific():
    mock_dk_pool = _build_mock_player_pool()

    roster = run(
        rule_set=rules.DK_NFL_SHOWDOWN_RULE_SET,
        player_pool=mock_dk_pool,
        optimizer_settings=OptimizerSettings(
            showdown_teams=('X', 'Y'),
            no_defense_against_captain=True,
        ),
        constraints=LineupConstraints(
            position_banned=['A1 CPT X'],
        ),
        verbose=True
    )
    ntools.assert_not_equal(roster, None)
    ntools.assert_equal(roster.projected(), 386.0)
    flex = [
        x for x in roster.players
        if x.pos == 'FLEX'
        and x.name == 'A1'
    ][0]
    ntools.assert_equal('A1', flex.name)
