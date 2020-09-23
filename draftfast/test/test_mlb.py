import os
from nose import tools as ntools
from draftfast.optimize import run
from draftfast import rules
from draftfast.csv_parse import salary_download

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
salary_file = '{}/data/dk-mlb-salaries.csv'.format(CURRENT_DIR)


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
    ntools.assert_not_equal(roster, None)
    ntools.assert_true('RP' in [x.pos for x in roster.players])
