import os
import unittest
from draftfast.optimize import run
from draftfast import rules
from draftfast.csv_parse import salary_download
from draftfast.orm import Player
from draftfast.settings import CustomRule, OptimizerSettings

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
salary_file = '{}/data/dk-mlb-salaries.csv'.format(CURRENT_DIR)

assertions = unittest.TestCase('__init__')


def test_mlb_dk():
    player_pool = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        game=rules.DRAFT_KINGS,
        ruleset=rules.DK_MLB_RULE_SET,
    )
    roster = run(
        rule_set=rules.DK_MLB_RULE_SET,
        player_pool=player_pool,
        verbose=True,
    )

    # Test general position limits
    assertions.assertNotEqual(roster, None)
    assertions.assertTrue('RP' in [x.pos for x in roster.players])


def test_five_batters_max():
    player_pool = [
        Player(pos='P', name='A', cost=5000, team='C'),
        Player(pos='P', name='B', cost=5000, team='B'),

        Player(pos='1B', name='C', cost=5000, team='C'),
        Player(pos='OF', name='H', cost=5000, team='C'),
        Player(pos='OF', name='I', cost=5000, team='C'),
        Player(pos='C', name='F', cost=5000, team='C'),
        Player(pos='2B', name='D', cost=5000, team='C'),
        Player(pos='2B', name='E', cost=5000, team='C'),
        Player(pos='3B', name='E', cost=5000, team='C'),

        Player(pos='SS', name='G', cost=5000, team='Q'),
        Player(pos='OF', name='J', cost=5000, team='G'),
    ]

    roster = run(
        rule_set=rules.DK_MLB_RULE_SET,
        player_pool=player_pool,
        verbose=True,
    )
    assert roster is None

    player_pool.append(Player(pos='3B', name='EA', cost=5000, team='A'))
    roster = run(
        rule_set=rules.DK_MLB_RULE_SET,
        player_pool=player_pool,
        verbose=True,
    )
    c_in_roster = [
        x for x in roster.players
        if x.team == 'C'
        and x.pos != 'P'
    ]

    assert len(c_in_roster) < 6


def test_custom_rules():
    # Minimum stack size
    custom_rules = []
    player_pool = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        game=rules.DRAFT_KINGS,
        ruleset=rules.DK_MLB_RULE_SET,
    )
    for p in player_pool:
        if p.team == 'ATL' and p.pos == '1B':
            p.proj = 1_000

    def comp(sum, a, b):
        return sum(b) >= sum(a) + 2

    # It appears to me closures do not work with ortools
    # (ex. passing p.team == t)
    custom_rules.append(
        CustomRule(
            # Given 1B in optimized lineup
            group_a=lambda p:
            p.pos == '1B' and p.team == 'ATL',

            # Ensure the stack is four players
            group_b=lambda p:
            '1B' not in p.pos and p.team == 'ATL',  # batters only

            comparison=comp,
        )
    )
    custom_rules.append(
        CustomRule(
            # Given 1B in optimized lineup
            group_a=lambda p:
            p.pos == '1B' and p.team == 'BOS',

            # Ensure the stack is four players
            group_b=lambda p:
            '1B' not in p.pos and p.team == 'BOS',  # batters only

            comparison=comp,
        )
    )

    settings = OptimizerSettings(
        custom_rules=custom_rules
    )

    roster = run(
        rule_set=rules.DK_MLB_RULE_SET,
        player_pool=player_pool,
        verbose=True,
        optimizer_settings=settings,
    )
    team_for_first = [p for p in roster.players if p.pos == '1B'][0].team
    total = len([p for p in roster.players
                 if p.team == team_for_first and 'P' not in p.pos])
    assert total > 3, f"{total} below 4"
