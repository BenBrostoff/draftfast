import os
from nose import tools as ntools
from draftfast.optimize import run
from draftfast import rules
from draftfast.csv_parse import salary_download
from draftfast.orm import Roster

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
salary_file = '{}/data/soccer-showdown.csv'.format(CURRENT_DIR)


class Showdown(Roster):
    POSITION_ORDER = {
        'M': 0,
        'F': 1,
        'D': 2,
        'GK': 3,
    }


showdown_limits = [
    ['M', 0, 6],
    ['F', 0, 6],
    ['D', 0, 6],
    ['GK', 0, 6],
]


def test_el_dk():
    soccer_rules = rules.RuleSet(
        site=rules.DRAFT_KINGS,
        league='SOCCER_SHOWDOWN',
        roster_size=6,
        position_limits=showdown_limits,
        salary_max=50_000,
        general_position_limits=[],
    )
    player_pool = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        game=rules.DRAFT_KINGS,
    )
    roster = run(
        rule_set=soccer_rules,
        player_pool=player_pool,
        verbose=True,
        roster_gen=Showdown,
    )
    ntools.assert_not_equal(roster, None)
