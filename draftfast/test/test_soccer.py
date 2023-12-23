import os
import unittest
from draftfast.optimize import run
from draftfast import rules
from draftfast.csv_parse import salary_download
from draftfast.settings import OptimizerSettings
from draftfast.lineup_constraints import LineupConstraints

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
salary_file = "{}/data/dk-soccer-salaries.csv".format(CURRENT_DIR)

assertions = unittest.TestCase("__init__")


def test_soccer_dk():
    player_pool = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        game=rules.DRAFT_KINGS,
    )
    roster = run(
        rule_set=rules.DK_SOCCER_RULE_SET,
        player_pool=player_pool,
        verbose=True,
    )
    assertions.assertNotEqual(roster, None)


def test_soccer_dk_no_opp_d():
    player_pool = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        game=rules.DRAFT_KINGS,
    )
    roster = run(
        rule_set=rules.DK_SOCCER_RULE_SET,
        player_pool=player_pool,
        constraints=LineupConstraints(
            locked=["Maxi Gomez"],
        ),
        optimizer_settings=OptimizerSettings(
            no_offense_against_defense=False,
        ),
        verbose=True,
    )
    cel_off_players = [
        p for p in roster.players if p.team == "CEL" and p.pos in ["M", "F"]
    ]
    lgn_d_players = [
        p for p in roster.players if p.team == "LGN" and p.pos in ["D", "GK"]
    ]
    assertions.assertEqual(len(cel_off_players), 2)
    assertions.assertEqual(len(lgn_d_players), 2)

    roster = run(
        rule_set=rules.DK_SOCCER_RULE_SET,
        player_pool=player_pool,
        constraints=LineupConstraints(
            locked=["Maxi Gomez"],
        ),
        optimizer_settings=OptimizerSettings(
            no_offense_against_defense=True,
        ),
        verbose=True,
    )
    cel_off_players = [
        p for p in roster.players if p.team == "CEL" and p.pos in ["M", "F"]
    ]
    lgn_d_players = [
        p for p in roster.players if p.team == "LGN" and p.pos in ["D", "GK"]
    ]
    assertions.assertEqual(len(cel_off_players), 2)
    assertions.assertEqual(len(lgn_d_players), 0)
