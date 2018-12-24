import os
from nose import tools as ntools
from draftfast.optimize import run
from draftfast import rules
from draftfast.csv_parse import salary_download
from draftfast.settings import OptimizerSettings, Stack

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
salary_file = '{}/data/dk-nhl-salaries.csv'.format(CURRENT_DIR)


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
    ntools.assert_not_equal(roster, None)


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
                Stack(team='TOR', count=3),
                Stack(team='COL', count=3),
                Stack(team='VAN', count=2),
            ]
        )
    )
    players = roster.sorted_players()

    phi_players = [x for x in players if x.team == 'TOR']
    fla_players = [x for x in players if x.team == 'COL']
    nsh_players = [x for x in players if x.team == 'VAN']
    ntools.assert_equal(len(phi_players), 3)
    ntools.assert_equal(len(fla_players), 3)
    ntools.assert_equal(len(nsh_players), 2)
