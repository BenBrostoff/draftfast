import os
import unittest
from draftfast.csv_parse import salary_download
from draftfast.rules import (
    DRAFT_KINGS,
    FAN_DUEL,
    FD_NFL_MVP_RULE_SET,
    FD_MLB_MVP_RULE_SET,
    FD_NBA_MVP_RULE_SET,
)
from draftfast.optimize import run

assertions = unittest.TestCase("__init__")

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
salaries = f"{CURRENT_DIR}/data/nba-test-salaries.csv"
projections = f"{CURRENT_DIR}/data/nba-test-projections.csv"
fd_mvp_nfl_salaries = f"{CURRENT_DIR}/data/nfl-mvp-fd-test-salaries.csv"
fd_mvp_mlb_salaries = f"{CURRENT_DIR}/data/mlb-mvp-fd-test-salaries.csv"
fd_mvp_nba_salaries = f"{CURRENT_DIR}/data/nba-mvp-fd-test-salaries.csv"


def test_dk_nba_parse():
    players = salary_download.generate_players_from_csvs(
        salary_file_location=salaries,
        game=DRAFT_KINGS,
    )
    assertions.assertEqual(len(players), 221)


def test_dk_nba_use_avg():
    players = salary_download.generate_players_from_csvs(
        salary_file_location=salaries,
        game=DRAFT_KINGS,
    )
    assertions.assertEqual(players[0].proj, 60.462)


def test_dk_nba_use_proj():
    players = salary_download.generate_players_from_csvs(
        salary_file_location=salaries,
        projection_file_location=projections,
        game=DRAFT_KINGS,
    )
    assertions.assertEqual(players[0].proj, 62.29)


def test_fd_showdown_nfl():
    players = salary_download.generate_players_from_csvs(
        salary_file_location=fd_mvp_nfl_salaries,
        projection_file_location=projections,
        game=FAN_DUEL,
        ruleset=FD_NFL_MVP_RULE_SET,
    )
    assertions.assertEqual(len(players), 146)

    # Two same ID players should break out captain and flex
    # and have identical costs
    renfrow = [p for p in players if p.name == "Hunter Renfrow"]
    assertions.assertEqual(len(renfrow), 2)
    assertions.assertEqual(renfrow[0].cost, renfrow[1].cost)
    assertions.assertAlmostEqual(
        renfrow[0].average_score, renfrow[1].average_score * 1.5
    )
    assertions.assertEqual(renfrow[0].pos, "CPT")
    assertions.assertEqual(renfrow[1].pos, "FLEX")

    # Optimization should work
    optimized = run(rule_set=FD_NFL_MVP_RULE_SET, player_pool=players)
    assertions.assertEqual(len(optimized.players), 5)


def test_fd_showdown_mlb():
    players = salary_download.generate_players_from_csvs(
        salary_file_location=fd_mvp_mlb_salaries,
        projection_file_location=projections,
        game=FAN_DUEL,
        ruleset=FD_MLB_MVP_RULE_SET,
    )
    assertions.assertEqual(len(players), 147)

    judges = [p for p in players if p.name == "Aaron Judge"]
    assertions.assertEqual(len(judges), 3)
    mvp, star, util = judges

    assertions.assertEqual(mvp.cost, star.cost, util.cost)
    assertions.assertEqual(mvp.pos, "MVP")
    assertions.assertEqual(star.pos, "STAR")
    assertions.assertEqual(util.pos, "UTIL")

    assertions.assertAlmostEqual(star.average_score, util.average_score * 1.5)
    assertions.assertAlmostEqual(mvp.average_score, util.average_score * 2)

    # Optimization should work
    optimized = run(rule_set=FD_MLB_MVP_RULE_SET, player_pool=players)
    assertions.assertEqual(len(optimized.players), 5)


def test_fd_showdown_nba():
    """
    Based on
    https://www.fanduel.com/games/76828/contests/76828-256975749/entries/2844624169/scoring?entry=2844624169
    """
    players = salary_download.generate_players_from_csvs(
        salary_file_location=fd_mvp_nba_salaries,
        projection_file_location=projections,
        game=FAN_DUEL,
        ruleset=FD_NBA_MVP_RULE_SET,
    )
    for p in players:
        p.proj = p.average_score

    assertions.assertEqual(len(players), 20)

    chefs = [p for p in players if p.name == "Stephen Curry"]
    assertions.assertEqual(len(chefs), 4)
    mvp, star, pro, util = chefs

    assertions.assertEqual(mvp.cost, star.cost, util.cost)
    assertions.assertEqual(mvp.pos, "MVP")
    assertions.assertEqual(star.pos, "STAR")
    assertions.assertEqual(pro.pos, "PRO")
    assertions.assertEqual(util.pos, "UTIL")

    assertions.assertAlmostEqual(pro.average_score, util.average_score * 1.2)
    assertions.assertAlmostEqual(star.average_score, util.average_score * 1.5)
    assertions.assertAlmostEqual(mvp.average_score, util.average_score * 2)

    # Optimization should work
    optimized = run(rule_set=FD_NBA_MVP_RULE_SET, player_pool=players)
    print(optimized)
    assertions.assertEqual(len(optimized.players), 5)
    assertions.assertAlmostEqual(optimized.projected(), 276.99)
