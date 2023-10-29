import os
from draftfast.optimize import run
from draftfast import rules
from draftfast.csv_parse import salary_download
from draftfast.showdown.orm import ShowdownPlayer

import unittest
assertions = unittest.TestCase('__init__')


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
salary_file = '{}/data/f1-salaries-showdown.csv'.format(CURRENT_DIR)


def test_f1_dk():
    player_pool = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        game=rules.DRAFT_KINGS,
        ruleset=rules.DK_F1_SHOWDOWN,
    )
    roster = run(
        rule_set=rules.DK_F1_SHOWDOWN,
        player_pool=player_pool,
        verbose=True,
    )
    assertions.assertNotEqual(roster, None)
    for p in roster.sorted_players():
        assertions.assertEquals(type(p), ShowdownPlayer)


def test_f1_identifier():
    player_pool = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        game=rules.DRAFT_KINGS,
        ruleset=rules.DK_F1_SHOWDOWN,
    )
    roster = run(
        rule_set=rules.DK_F1_SHOWDOWN,
        player_pool=player_pool,
        verbose=True,
    )
    assertions.assertNotEqual(roster.identifier, None)
