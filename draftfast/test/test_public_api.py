from nose import tools as ntools
from draftfast.optimize import beta_run
from draftfast.rules import DK_NBA_RULE_SET
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

def test_simple():
    roster = beta_run(
        rule_set=DK_NBA_RULE_SET,
        players=mock_player_pool,
    )
    ntools.assert_not_equals(roster, None)