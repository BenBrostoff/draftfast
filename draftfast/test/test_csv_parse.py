import os
from nose import tools as ntools
from draftfast.csv_parse import salary_download
from draftfast.rules import DRAFT_KINGS, FAN_DUEL, FD_NFL_MVP_RULE_SET

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
salaries = f'{CURRENT_DIR}/data/nba-test-salaries.csv'
projections = f'{CURRENT_DIR}/data/nba-test-projections.csv'
fd_mvp_salaries = f'{CURRENT_DIR}/data/nfl-mvp-fd-test-salaries.csv'


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


def test_fd_showdown_nba():
    players = salary_download.generate_players_from_csvs(
        salary_file_location=salaries,
        projection_file_location=projections,
        game=FAN_DUEL,
        ruleset=FD_NFL_MVP_RULE_SET,
    )
    ntools.assert_equals(len(players), 1)