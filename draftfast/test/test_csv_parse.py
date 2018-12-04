import os
from nose import tools as ntools
from draftfast.csv_parse import salary_download
from draftfast.rules import DRAFT_KINGS

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
salaries = '{}/data/nba-test-salaries.csv'.format(CURRENT_DIR)
projections = '{}/data/nba-test-projections.csv'.format(CURRENT_DIR)


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
