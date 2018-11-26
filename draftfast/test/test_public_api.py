from nose import tools as ntools
from draftfast.optimize import beta_run
from draftfast import rules
from draftfast.orm import Player

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

def test_nba_dk():
    roster = beta_run(
        rule_set=rules.DK_NBA_RULE_SET,
        players=mock_player_pool,
        verbose=True,
    )
    ntools.assert_not_equals(roster, None)

def test_nba_dk_with_csv():
    roster = beta_run(
        rule_set=rules.DK_NBA_RULE_SET,
        players=mock_player_pool,
        verbose=True,
    )
    ntools.assert_not_equals(roster, None)

def test_nba_fd():
    roster = beta_run(
        rule_set=rules.FD_NBA_RULE_SET,
        players=mock_player_pool,
    )
    ntools.assert_not_equals(roster, None)

def test_nfl_dk():
    roster = beta_run(
        rule_set=rules.DK_NFL_RULE_SET,
        players=mock_player_pool,
    )
    ntools.assert_not_equals(roster, None)

def test_nfl_fd():
    roster = beta_run(
        rule_set=rules.FD_NFL_RULE_SET,
        players=mock_player_pool,
    )
    ntools.assert_not_equals(roster, None)
