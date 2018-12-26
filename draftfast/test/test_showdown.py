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

def _build_mock_player_pool():
    player_pool = [
        Player(name='A1', cost=5500, proj=60, pos='QB',
                                team='X', matchup='X@Y'),
        Player(name='A2', cost=5500, proj=41, pos='QB',
                                team='X', matchup='X@Y'),
        Player(name='A11', cost=5500, proj=50, pos='WR',
                                team='X', matchup='X@Y'),
        Player(name='A3', cost=5500, proj=42, pos='WR',
                                team='X', matchup='X@Y'),
        Player(name='A4', cost=5500, proj=43, pos='WR',
                                team='X', matchup='X@Y'),
        Player(name='A5', cost=5500, proj=44, pos='WR',
                                team='X', matchup='X@Y'),
        Player(name='A6', cost=5500, proj=45, pos='RB',
                                team='X', matchup='X@Y'),
        Player(name='A7', cost=5500, proj=46, pos='RB',
                                team='X', matchup='X@Y'),
        Player(name='A8', cost=5500, proj=47, pos='RB',
                                team='X', matchup='X@Y'),
        Player(name='A9', cost=5500, proj=48, pos='TE',
                                team='X', matchup='X@Y'),
        Player(name='A10', cost=5500, proj=49, pos='TE',
                                team='X', matchup='X@Y'),
        Player(name='A12', cost=5500, proj=51, pos='DST',
                                team='X', matchup='X@Y'),
        Player(name='A14', cost=5500, proj=40, pos='QB',
                                team='Y', matchup='X@Y'),
        Player(name='A21', cost=5500, proj=41, pos='QB',
                                team='Y', matchup='X@Y'),
        Player(name='A11', cost=5500, proj=50, pos='WR',
                                team='Y', matchup='X@Y'),
        Player(name='A31', cost=5500, proj=42, pos='WR',
                                team='Y', matchup='X@Y'),
        Player(name='A41', cost=5500, proj=43, pos='WR',
                                team='Y', matchup='X@Y'),
        Player(name='A51', cost=5500, proj=54, pos='WR',
                                team='Y', matchup='X@Y'),
        Player(name='A61', cost=5500, proj=45, pos='RB',
                                team='Y', matchup='X@Y'),
        Player(name='A71', cost=5500, proj=56, pos='RB',
                                team='Y', matchup='X@Y'),
        Player(name='A81', cost=5500, proj=47, pos='RB',
                                team='Y', matchup='X@Y'),
        Player(name='A91', cost=5500, proj=48, pos='TE',
                                team='Y', matchup='X@Y'),
        Player(name='A110', cost=5500, proj=49, pos='TE',
                                team='Y', matchup='X@Y'),
        Player(name='A112', cost=5500, proj=51, pos='DST',
                                team='Y', matchup='X@Y'),
    ]

    mock_dk_pool = [ShowdownPlayer(p) for p in player_pool] + \
                   [ShowdownPlayer(p, captain=True) for p in player_pool]

    return mock_dk_pool


def test_nfl_dk_showdown_mock():
    mock_dk_pool = _build_mock_player_pool()

    roster = run(
        rule_set=rules.DK_NFL_SHOWDOWN_RULE_SET,
        player_pool=mock_dk_pool,
        optimizer_settings=OptimizerSettings(
            showdown_teams=('X', 'Y'),
        ),
        verbose=True
    )

    ntools.assert_not_equal(roster, None)
    ntools.assert_equal(roster.projected(), 352.0)

@ntools.raises(NotImplementedError)
def test_nfl_showdown_no_def_against_capt():
    mock_dk_pool = _build_mock_player_pool()

    roster = run(
        rule_set=rules.DK_NFL_SHOWDOWN_RULE_SET,
        player_pool=mock_dk_pool,
        optimizer_settings=OptimizerSettings(
            showdown_teams=('X', 'Y'),
            no_defense_against_captain=True,
        ),
        verbose=True
    )

    ntools.assert_not_equal(roster, None)
    ntools.assert_equal(roster.projected(), 352.0)

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
#         optimizer_settings=OptimizerSettings(
#             showdown_teams=('GB', 'JAX'),
#         ),
#         verbose=True
#     )

#     ntools.assert_not_equal(roster, None)
#     ntools.assert_equal(roster.projected(), 117.60)
