import os
from copy import deepcopy
from nose import tools as ntools
from draftfast.optimize import run
from draftfast import rules
from draftfast.orm import Player
from draftfast.csv_parse import salary_download
from draftfast.settings import OptimizerSettings, Stack
from draftfast.lineup_constraints import LineupConstraints
from draftfast.settings import OptimizerSettings, CustomRule

mock_nba_pool = [
    Player(name='A1', cost=5500, proj=100, pos='PG'),
    Player(name='A2', cost=5500, proj=41, pos='PG'),
    Player(name='A11', cost=5500, proj=50, pos='PG'),
    Player(name='A3', cost=5500, proj=42, pos='SG'),
    Player(name='A4', cost=5500, proj=0, pos='SG'),
    Player(name='A5', cost=5500, proj=44, pos='SF'),
    Player(name='A6', cost=5500, proj=45, pos='SF'),
    Player(name='A7', cost=5500, proj=46, pos='PF'),
    Player(name='A8', cost=5500, proj=47, pos='PF'),
    Player(name='A9', cost=5500, proj=0, pos='C'),
    Player(name='A10', cost=5500, proj=49, pos='C'),
]

def test_nba_dk():
    settings = OptimizerSettings(
      custom_rules=[
        # Always play A1 with A9 and A4
        CustomRule(
          group_a=lambda x: p.name == 'A1',
          group_b=lambda x: x.name == 'A9' or x.name == 'A4'
        )
      ]
    )

    # TODO - add test where A1 is not in optimized lineup
    roster = run(
        rule_set=rules.DK_NBA_RULE_SET,
        player_pool=mock_nba_pool,
        verbose=True,
        optimizer_settings=settings,
    )
    names = {p.name for p in roster.players}
    
    # Without this rule, A4 and A9 would never appear in the optimized
    # lineup. Both have a 0 point projection.
    ntools.assert_equal(
      True,
      'A1' in names and 'A9' in names and 'A4' in names
    )
