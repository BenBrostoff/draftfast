from draftfast.optimize import run
from draftfast import rules
from draftfast.orm import Player

import unittest
assertions = unittest.TestCase('__init__')

GOLFER, CPT = 'G', 'CPT'


def test_golf_dk():
    player_pool = [
        Player(name='G1', cost=5500, proj=55, pos=GOLFER),
        Player(name='G2', cost=5600, proj=55, pos=GOLFER),
        Player(name='G3', cost=5700, proj=55, pos=GOLFER),
        Player(name='G4', cost=5800, proj=55, pos=GOLFER),
        Player(name='G5', cost=5800, proj=55, pos=GOLFER),
        Player(name='G6', cost=5900, proj=55, pos=GOLFER),
        Player(name='G7', cost=10000, proj=155, pos=GOLFER),
    ]
    roster = run(
        rule_set=rules.DK_PGA_RULE_SET,
        player_pool=player_pool,
        verbose=True,
    )
    assertions.assertNotEqual(roster, None)


def test_golf_dk_captain():
    player_pool = [
        Player(name='G1', cost=5500, proj=1, pos=CPT),
        Player(name='G2', cost=5600, proj=55, pos=GOLFER),
        Player(name='G3', cost=5700, proj=55, pos=GOLFER),
        Player(name='G4', cost=5800, proj=55, pos=GOLFER),
        Player(name='G5', cost=5800, proj=55, pos=GOLFER),
        Player(name='G6', cost=5900, proj=55, pos=GOLFER),
        Player(name='G7', cost=10000, proj=155, pos=GOLFER),
    ]
    roster = run(
        rule_set=rules.DK_PGA_SHOWDOWN_CAPTAIN_RULE_SET,
        player_pool=player_pool,
        verbose=True,
    )
    assertions.assertNotEqual(roster, None)
    assertions.assertEquals(roster.projected(), 376)
