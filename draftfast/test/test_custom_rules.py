from draftfast.optimize import run
from draftfast import rules
from draftfast.orm import Player
from draftfast.settings import OptimizerSettings, CustomRule

import unittest

assertions = unittest.TestCase("__init__")


def construct_pool():
    mock_nba_pool = [
        Player(name="A1", cost=5500, proj=100, pos="PG", matchup="AvB"),
        Player(name="A2", cost=5500, proj=41, pos="PG", matchup="AvB"),
        Player(name="A100", cost=5500, proj=501, pos="PG", matchup="AvB"),
        Player(name="A101", cost=5500, proj=500, pos="PG", matchup="AvB"),
        Player(name="A11", cost=5500, proj=50, pos="PG", matchup="AvB"),
        Player(name="A3", cost=5500, proj=42, pos="SG", matchup="AvB"),
        Player(name="A4", cost=5500, proj=0, pos="SG", matchup="CvD"),
        Player(name="A5", cost=5500, proj=44, pos="SF", matchup="CvD"),
        Player(name="A6", cost=5500, proj=45, pos="SF", matchup="CvD"),
        Player(name="A7", cost=5500, proj=46, pos="PF", matchup="CvD"),
        Player(name="A8", cost=5500, proj=47, pos="PF", matchup="CvD"),
        Player(name="A9", cost=5500, proj=0, pos="C", matchup="CvD"),
        Player(name="A10", cost=5500, proj=49, pos="C", matchup="CvD"),
    ]

    team = 0
    for p in mock_nba_pool:
        team += 1
        if p.name in ["A101", "A100", "A10"]:
            p.team = "SomeTeam"
        else:
            p.team = str(team)

    return mock_nba_pool


def test_if_one_then_one():
    mock_nba_pool = construct_pool()
    # Base case
    roster = run(
        rule_set=rules.DK_NBA_RULE_SET,
        player_pool=mock_nba_pool,
        verbose=True,
    )
    names = {p.name for p in roster.players}
    assertions.assertEqual(True, "A1" in names and "A4" not in names)
    settings = OptimizerSettings(
        custom_rules=[
            # Always play A1 with A9 and A4
            CustomRule(
                group_a=lambda p: p.name == "A1",
                group_b=lambda p: p.name == "A4",
                comparison=lambda s_sum, a, b: s_sum(a) == s_sum(b),
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

    # Without this rule, A1 and A4 are not in the same lineup.
    assertions.assertEqual(True, "A1" in names and "A4" in names)

    # Confirm now that the rule prevents one without the other
    mock_nba_pool = construct_pool()
    for p in mock_nba_pool:
        if p.name == "A1":
            # A1 normally would always be in the lineup
            # due to highest projection among PGs
            p.proj = 502
        if p.name == "A4":
            # A4 projection is so negative it should
            # never be in any lineup
            p.proj = -1_000_000

    roster = run(
        rule_set=rules.DK_NBA_RULE_SET,
        player_pool=mock_nba_pool,
        verbose=True,
        optimizer_settings=settings,
    )
    names = {p.name for p in roster.players}
    assertions.assertEqual(True, "A1" not in names and "A4" not in names)


def test_if_one_then_two():
    mock_nba_pool = construct_pool()

    # Base case
    roster = run(
        rule_set=rules.DK_NBA_RULE_SET,
        player_pool=mock_nba_pool,
        verbose=True,
    )
    names = {p.name for p in roster.players}
    assertions.assertEqual(
        True, "A1" in names and "A4" not in names and "A9" not in names
    )
    settings = OptimizerSettings(
        custom_rules=[
            # Always play A1 with A9 and A4
            CustomRule(
                group_a=lambda p: p.name == "A1",
                group_b=lambda p: p.name == "A9" or p.name == "A4",
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
    assertions.assertEqual(
        True, "A1" in names and "A9" in names and "A4" in names
    )


def test_never_two():
    mock_nba_pool = construct_pool()

    # Base case
    roster = run(
        rule_set=rules.DK_NBA_RULE_SET,
        player_pool=mock_nba_pool,
        verbose=True,
    )
    names = {p.name for p in roster.players}
    assertions.assertEqual(True, "A101" in names and "A100" in names)

    # Never play two players together
    settings = OptimizerSettings(
        custom_rules=[
            CustomRule(
                group_a=lambda p: p,
                group_b=lambda p: p.name == "A100" or p.name == "A101",
                comparison=lambda sum, a, b: sum(b) <= 1,
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
    assertions.assertEqual(True, "A101" not in names and "A100" in names)


def test_team_rules():
    mock_nba_pool = construct_pool()

    # If two PGs on one team, play the C from same team
    settings = OptimizerSettings(
        custom_rules=[
            CustomRule(
                group_a=lambda p: p.pos == "C" and p.team == "SomeTeam",
                group_b=lambda p: p.pos == "PG" and p.team == "SomeTeam",
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
    assertions.assertEqual(
        True, "A100" in names and "A101" in names and "A10" in names
    )
