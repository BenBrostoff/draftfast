import os
from nose import tools as ntools
from draftfast.optimize import run, run_multi
from draftfast import rules
from draftfast.orm import Player
from draftfast.csv_parse import salary_download
from draftfast.settings import OptimizerSettings, Stack
from draftfast.lineup_contraints import LineupConstraints
from draftfast.showdown.orm import ShowdownPlayer

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
salary_file = '{}/data/dk-nfl-salaries.csv'.format(CURRENT_DIR)
fd_nfl_salary_file = '{}/data/fd-nfl-salaries.csv'.format(CURRENT_DIR)
projection_file = '{}/data/dk-nfl-projections.csv'.format(CURRENT_DIR)


# def test_nfl_dk_showdown_mock():
#     mock_dk_pool = [
#         ShowdownPlayer(Player(name='A1', cost=5500, proj=40, pos='QB')),
#         ShowdownPlayer(Player(name='A2', cost=5500, proj=41, pos='QB')),
#         ShowdownPlayer(Player(name='A11', cost=5500, proj=50, pos='WR')),
#         ShowdownPlayer(Player(name='A3', cost=5500, proj=42, pos='WR')),
#         ShowdownPlayer(Player(name='A4', cost=5500, proj=43, pos='WR')),
#         ShowdownPlayer(Player(name='A5', cost=5500, proj=44, pos='WR')),
#         ShowdownPlayer(Player(name='A6', cost=5500, proj=45, pos='RB')),
#         ShowdownPlayer(Player(name='A7', cost=5500, proj=46, pos='RB')),
#         ShowdownPlayer(Player(name='A8', cost=5500, proj=47, pos='RB')),
#         ShowdownPlayer(Player(name='A9', cost=5500, proj=48, pos='TE')),
#         ShowdownPlayer(Player(name='A10', cost=5500, proj=49, pos='TE')),
#         ShowdownPlayer(Player(name='A12', cost=5500, proj=51, pos='DST')),
#         ShowdownPlayer(Player(name='A13', cost=5500, proj=52, pos='DST')),
#     ]
#     for p in mock_dk_pool:
#         mock_dk_pool.append(ShowdownPlayer(p, captain=True))

#     roster = run(
#         rule_set=rules.DK_NFL_SHOWDOWN_RULE_SET,
#         player_pool=mock_dk_pool,
#     )

#     ntools.assert_not_equal(roster, None)
#     ntools.assert_equal(roster.projected(), 420.0)


# def test_nfl_dk():
#     players = salary_download.generate_players_from_csvs(
#         salary_file_location=salary_file,
#         projection_file_location=projection_file,
#         game=rules.DRAFT_KINGS,
#         ruleset=rules.DK_NFL_SHOWDOWN_RULE_SET
#     )
#     roster = run(
#         rule_set=rules.DK_NFL_SHOWDOWN_RULE_SET,
#         player_pool=players,
#         verbose=True
#     )

#     ntools.assert_not_equal(roster, None)
#     ntools.assert_equal(roster.projected(), 117.60)
