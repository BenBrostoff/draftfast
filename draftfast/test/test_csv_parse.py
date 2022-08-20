import os
from nose import tools as ntools
from draftfast.csv_parse import salary_download
from draftfast.rules import (
    DRAFT_KINGS, FAN_DUEL,
    FD_NFL_MVP_RULE_SET, FD_MLB_MVP_RULE_SET,
    FD_NBA_MVP_RULE_SET
)
from draftfast.optimize import run

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
salaries = f'{CURRENT_DIR}/data/nba-test-salaries.csv'
projections = f'{CURRENT_DIR}/data/nba-test-projections.csv'
fd_mvp_nfl_salaries = f'{CURRENT_DIR}/data/nfl-mvp-fd-test-salaries.csv'
fd_mvp_mlb_salaries = f'{CURRENT_DIR}/data/mlb-mvp-fd-test-salaries.csv'
fd_mvp_nba_salaries = f'{CURRENT_DIR}/data/nba-mvp-fd-test-salaries.csv'


def test_dk_nba_parse():
    players = salary_download.generate_players_from_csvs(
        salary_file_location=salaries,
        game=DRAFT_KINGS,
    )
    ntools.assert_equals(len(players), 221)


def test_dk_nba_use_avg():
    players = salary_download.generate_players_from_csvs(
        salary_file_location=salaries,
        game=DRAFT_KINGS,
    )
    ntools.assert_equals(players[0].proj, 60.462)


def test_dk_nba_use_proj():
    players = salary_download.generate_players_from_csvs(
        salary_file_location=salaries,
        projection_file_location=projections,
        game=DRAFT_KINGS,
    )
    ntools.assert_equals(players[0].proj, 62.29)


def test_fd_showdown_nfl():
    players = salary_download.generate_players_from_csvs(
        salary_file_location=fd_mvp_nfl_salaries,
        projection_file_location=projections,
        game=FAN_DUEL,
        ruleset=FD_NFL_MVP_RULE_SET,
    )
    ntools.assert_equals(len(players), 146)

    # Two same ID players should break out captain and flex
    # and have identical costs
    renfrow = [
        p for p in players
        if p.name == 'Hunter Renfrow'
    ]
    ntools.assert_equals(len(renfrow), 2)
    ntools.assert_equals(renfrow[0].cost, renfrow[1].cost)
    ntools.assert_almost_equals(
        renfrow[0].average_score,
        renfrow[1].average_score * 1.5
    )
    ntools.assert_equals(renfrow[0].pos, 'CPT')
    ntools.assert_equals(renfrow[1].pos, 'FLEX')

    # Optimization should work
    optimized = run(
        rule_set=FD_NFL_MVP_RULE_SET,
        player_pool=players
    )
    ntools.assert_equals(len(optimized.players), 5)


def test_fd_showdown_mlb():
    players = salary_download.generate_players_from_csvs(
        salary_file_location=fd_mvp_mlb_salaries,
        projection_file_location=projections,
        game=FAN_DUEL,
        ruleset=FD_MLB_MVP_RULE_SET,
    )
    ntools.assert_equals(len(players), 147)

    judges = [
        p for p in players
        if p.name == 'Aaron Judge'
    ]
    ntools.assert_equals(len(judges), 3)
    mvp, star, util = judges

    ntools.assert_equals(mvp.cost, star.cost, util.cost)
    ntools.assert_equals(mvp.pos, 'MVP')
    ntools.assert_equals(star.pos, 'STAR')
    ntools.assert_equals(util.pos, 'UTIL')

    ntools.assert_almost_equals(
        star.average_score,
        util.average_score * 1.5
    )
    ntools.assert_almost_equals(
        mvp.average_score,
        util.average_score * 2
    )

    # Optimization should work
    optimized = run(
        rule_set=FD_MLB_MVP_RULE_SET,
        player_pool=players
    )
    ntools.assert_equals(len(optimized.players), 5)


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

    ntools.assert_equals(len(players), 20)

    chefs = [
        p for p in players
        if p.name == 'Stephen Curry'
    ]
    ntools.assert_equals(len(chefs), 4)
    mvp, star, pro, util = chefs

    ntools.assert_equals(mvp.cost, star.cost, util.cost)
    ntools.assert_equals(mvp.pos, 'MVP')
    ntools.assert_equals(star.pos, 'STAR')
    ntools.assert_equals(pro.pos, 'PRO')
    ntools.assert_equals(util.pos, 'UTIL')

    ntools.assert_almost_equals(
        pro.average_score,
        util.average_score * 1.2
    )
    ntools.assert_almost_equals(
        star.average_score,
        util.average_score * 1.5
    )
    ntools.assert_almost_equals(
        mvp.average_score,
        util.average_score * 2
    )

    # Optimization should work
    optimized = run(
        rule_set=FD_NBA_MVP_RULE_SET,
        player_pool=players
    )
    print(optimized)
    ntools.assert_equals(len(optimized.players), 5)
    ntools.assert_almost_equals(optimized.projected(), 276.99)
