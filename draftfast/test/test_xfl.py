import os
import unittest
from draftfast.optimize import run
from draftfast import rules
from draftfast.csv_parse import salary_download

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
salary_file = "{}/data/dk-xfl-salaries.csv".format(CURRENT_DIR)


assertions = unittest.TestCase("__init__")


def test_xlf_lineup():
    player_pool = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        game=rules.DRAFT_KINGS,
    )
    roster = run(
        rule_set=rules.DK_XFL_CLASSIC_RULE_SET,
        player_pool=player_pool,
        verbose=True,
    )
    assertions.assertNotEqual(roster, None)
