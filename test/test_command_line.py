import os
from nose import tools as ntools
from optimize import run
from argparse import Namespace
from collections import Counter

NFL = 'NFL'
args_dict = dict(
    game='draftkings',
    dtype='wr',
    duo='n',
    i=1,
    season=2016,
    w=1,
    historical='n',
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
    source='nfl_rotogrinders',
    salary_file=os.getcwd() + '/test/data/test-salaries.csv',
    projection_file=os.getcwd() + '/test/data/test-projections.csv',
    flex_position=None,
    min_avg=-1,
    historical_date=None,
)


def test_default_constraints():
    args = Namespace(**args_dict)
    roster = run(NFL, args)
    assert roster


def test_multi_position():
    args = Namespace(**args_dict)
    args.locked = ['Eli Manning']
    roster = run(NFL, args)
    multi_pos = [p for p in roster.players if p.name == 'Eli Manning']
    ntools.assert_equal(len(multi_pos), 1)
    ntools.assert_equal(multi_pos[0].pos, 'TE')


def test_is_home():
    args = Namespace(**args_dict)
    args.home = True
    roster = run(NFL, args)
    for p in roster.players:
        ntools.assert_true(p.is_home)


def test_within_avg():
    args = Namespace(**args_dict)
    avg_test_val = 3
    args.v_avg = avg_test_val
    roster = run(NFL, args)
    for player in roster.players:
        ntools.assert_less(abs(player.v_avg), avg_test_val)


def test_duo_constraint():
    args = Namespace(**args_dict)
    args.duo = 'NE'
    roster = run(NFL, args)
    team_instances = Counter([p.team for p in roster.players]).values()
    ntools.assert_in(2, team_instances)


def test_min_salary():
    args = Namespace(**args_dict)
    args.sp = 3500
    roster = run(NFL, args)
    for p in roster.players:
        ntools.assert_true(p.cost >= 3500)


def test_teams_constraint():
    args = Namespace(**args_dict)
    args.teams = ['NE', 'Dal']
    roster = run(NFL, args)
    for p in roster.players:
        if p.pos == 'DST':
            continue
        ntools.assert_true(p.team == 'NE' or p.team == 'Dal')


def test_banned_constraint():
    args = Namespace(**args_dict)
    jg = 'Jimmy Garoppolo'
    args.teams = ['NE', 'Dal']
    args.banned = [jg]
    roster = run(NFL, args)
    ntools.assert_not_in(jg, [p.name for p in roster.players])


def test_locked_constraint():
    args = Namespace(**args_dict)
    jb = 'Jacoby Brissett'
    args.teams = ['NE', 'Dal']
    args.banned = []
    args.locked = [jb]
    roster = run(NFL, args)
    ntools.assert_true([p for p in roster.players if p.name == jb][0].lock)


def test_lock_overrides():
    args = Namespace(**args_dict)
    args.teams = ['NE', 'Dal']
    args.v_avg = 1
    args.locked = ['Eli Manning']
    roster = run(NFL, args)
    ntools.assert_true(
        [
            p for p in roster.players
            if p.name == 'Eli Manning'
        ][0].lock
    )


def test_bad_constraints():
    args = Namespace(**args_dict)
    args.lp = 1000
    roster = run(NFL, args)
    ntools.assert_equal(roster, None)


def test_multi_roster():
    args = Namespace(**args_dict)
    roster = run(NFL, args)
    second_roster = run(NFL, args, [roster])
    ntools.assert_not_equals(roster == second_roster, True)
