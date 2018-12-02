import os
from nose import tools as ntools
from draftfast.optimize import run, run_multi
from argparse import Namespace

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

NFL = 'NFL'
args_dict = dict(
    game='draftkings',
    i=1,
    season=2016,
    w=1,
    league='NFL',
    limit='n',
    lp=0,
    no_double_te='n',
    mp=300,
    ms=10000,
    s='n',
    sp=3000,
    home=None,
    locked=None,
    teams=None,
    banned=None,
    po=0,
    po_location=None,
    v_avg=10000,
    test_mode=True,
    salary_file='{}/data/test-salaries.csv'.format(CURRENT_DIR),
    projection_file='{}/data/test-projections.csv'.format(CURRENT_DIR),
    flex_position=None,
    min_avg=-1,
    historical_date=None,
    pids=None,
    random_exposure='n',
)


def test_multi_position():
    args = Namespace(**args_dict)
    args.locked = ['Eli Manning']
    roster = run(NFL, args)
    multi_pos = [p for p in roster.players if p.name == 'Eli Manning']
    ntools.assert_equal(len(multi_pos), 1)
    ntools.assert_equal(multi_pos[0].pos, 'TE')


def test_within_avg():
    args = Namespace(**args_dict)
    avg_test_val = 3
    args.v_avg = avg_test_val
    roster = run(NFL, args)
    for player in roster.players:
        ntools.assert_less(abs(player.v_avg), avg_test_val)


def test_teams_constraint():
    args = Namespace(**args_dict)
    args.teams = ['NE', 'Dal']
    roster = run(NFL, args)
    for p in roster.players:
        if p.pos == 'DST':
            continue
        ntools.assert_true(p.team == 'NE' or p.team == 'Dal')


def test_deterministic_exposure_limits():
    args = Namespace(**args_dict)
    args.i = 2
    args.exposure_limit_file = \
        '{}/test/data/exposures.csv' \
        .format(os.getcwd())
    rosters, exposure_diffs = run_multi(args)
    ntools.assert_equal(len(rosters), args.i)
    ntools.assert_equal(len(exposure_diffs), 0)

    players = [p.name for p in rosters[0].players]
    ntools.assert_true('Andrew Luck' in players)
    ntools.assert_true('Alshon Jeffery' in players)

    players = [p.name for p in rosters[1].players]
    ntools.assert_true('Andrew Luck' not in players)
    ntools.assert_true('Alshon Jeffery' in players)


def test_random_exposure_limits():
    args = Namespace(**args_dict)
    args.i = 10
    args.random_exposure = 'y'
    args.exposure_random_seed = 42
    args.exposure_limit_file = \
        '{}/test/data/exposures.csv' \
        .format(os.getcwd())
    rosters, exposure_diffs = run_multi(args)
    ntools.assert_equal(len(rosters), args.i)
    ntools.assert_equal(len(exposure_diffs), 0)
