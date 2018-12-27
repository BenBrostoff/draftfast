import os
from nose import tools as ntools
from draftfast.optimize import run
from draftfast import rules
from draftfast.csv_parse import salary_download

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
salary_file = '{}/data/dk-euro-league-salaries.csv'.format(CURRENT_DIR)


def test_el_dk():
    player_pool = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        game=rules.DRAFT_KINGS,
    )
    roster = run(
        rule_set=rules.DK_EURO_LEAGUE_RULE_SET,
        player_pool=player_pool,
        verbose=True,
    )
    ntools.assert_not_equal(roster, None)
