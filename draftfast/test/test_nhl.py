import os
import unittest
from draftfast.optimize import run
from draftfast import rules
from draftfast.csv_parse import salary_download
from draftfast.settings import OptimizerSettings, Stack

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
salary_file = "{}/data/dk-nhl-salaries.csv".format(CURRENT_DIR)

assertions = unittest.TestCase("__init__")


def test_nhl_dk():
    player_pool = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        game=rules.DRAFT_KINGS,
        ruleset=rules.DK_NHL_RULE_SET,
    )
    roster = run(
        rule_set=rules.DK_NHL_RULE_SET,
        player_pool=player_pool,
        verbose=True,
    )
    assertions.assertNotEqual(roster, None)


def test_nhl_dk_unsolvable_three_team_non_goalie_restriction():
    """
    Should not solve if unable to get min teams of 3
    not including goalie team
    """
    player_pool = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        game=rules.DRAFT_KINGS,
        ruleset=rules.DK_NHL_RULE_SET,
    )
    unique_teams = set()
    new_player_pool = []
    for p in player_pool:
        if len(unique_teams) > 2 and p.team not in unique_teams:
            continue

        if p.pos != 'G':
            unique_teams.add(p.team)

        if len(unique_teams) < 3:
            new_player_pool.append(p)

    assertions.assertEqual(len(unique_teams) > 2, True)

    roster = run(
        rule_set=rules.DK_NHL_RULE_SET,
        player_pool=new_player_pool,
        verbose=True,
    )
    assertions.assertEqual(roster, None)


def test_triple_stack():
    player_pool = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        game=rules.DRAFT_KINGS,
        ruleset=rules.DK_NHL_RULE_SET,
    )
    roster = run(
        rule_set=rules.DK_NHL_RULE_SET,
        player_pool=player_pool,
        verbose=True,
        optimizer_settings=OptimizerSettings(
            stacks=[
                Stack(team="TOR", count=3),
                Stack(team="COL", count=3),
                Stack(team="VAN", count=2),
            ]
        ),
    )
    players = roster.sorted_players()

    phi_players = [x for x in players if x.team == "TOR"]
    fla_players = [x for x in players if x.team == "COL"]
    nsh_players = [x for x in players if x.team == "VAN"]
    assertions.assertEqual(len(phi_players), 3)
    assertions.assertEqual(len(fla_players), 3)
    assertions.assertEqual(len(nsh_players), 2)
