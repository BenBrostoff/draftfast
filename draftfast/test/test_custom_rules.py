from nose import tools as ntools
from draftfast.optimize import run
from draftfast import rules
from draftfast.orm import Player
from draftfast.settings import OptimizerSettings, CustomRule

mock_nba_pool = [
    Player(name='A1', cost=5500, proj=100, pos='PG'),
    Player(name='A2', cost=5500, proj=41, pos='PG'),
    Player(name='A100', cost=5500, proj=501, pos='PG'),
    Player(name='A101', cost=5500, proj=500, pos='PG'),
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

team = 0
for p in mock_nba_pool:
    team += 1
    if p.name in ['A101', 'A100', 'A10']:
        p.team = 'SomeTeam'
    else:
        p.team = str(team)


def test_if_one_then_two():
    # Base case
    roster = run(
        rule_set=rules.DK_NBA_RULE_SET,
        player_pool=mock_nba_pool,
        verbose=True,
    )
    names = {p.name for p in roster.players}
    ntools.assert_equal(
        True,
        'A1' in names and 'A4' not in names and 'A9' not in names
    )
    settings = OptimizerSettings(
        custom_rules=[
            # Always play A1 with A9 and A4
            CustomRule(
                group_a=lambda p: p.name == 'A1',
                group_b=lambda p: p.name == 'A9' or p.name == 'A4'
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


def test_never_two():
    # Base case
    roster = run(
        rule_set=rules.DK_NBA_RULE_SET,
        player_pool=mock_nba_pool,
        verbose=True,
    )
    names = {p.name for p in roster.players}
    ntools.assert_equal(
        True,
        'A101' in names and 'A100' in names
    )

    # Never play two players together
    settings = OptimizerSettings(
        custom_rules=[
          CustomRule(
              group_a=lambda p: p,
              group_b=lambda p: p.name == 'A100' or p.name == 'A101',
              comparison=lambda sum, a, b: sum(b) <= 1
          )
        ]
    )

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
        'A101' not in names and 'A100' in names
    )


def test_team_rules():
    # If two PGs on one team, play the C from same team
    settings = OptimizerSettings(
        custom_rules=[
            CustomRule(
                group_a=lambda p: p.pos == 'C' and p.team == 'SomeTeam',
                group_b=lambda p: p.pos == 'PG' and p.team == 'SomeTeam',
            )
        ]
    )
    roster = run(
        rule_set=rules.DK_NBA_RULE_SET,
        player_pool=mock_nba_pool,
        verbose=True,
        optimizer_settings=settings,
    )
    names = {p.name for p in roster.players}
    ntools.assert_equal(
        True,
        'A100' in names and 'A101' in names and 'A10' in names
    )
