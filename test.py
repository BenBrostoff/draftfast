from optimize import run
from constants import POSITIONS
from argparse import Namespace
from collections import Counter

NFL = 'NFL'
default_args = Namespace(
    dtype='wr', duo='n', i=3,
    l='NFL', limit='n', lp=0,
    mp=100, ms=10000, s='n', sp=3000, w='1',
    teams=None, banned=None)


def test_default_constraints():
    roster = run(POSITIONS[NFL], NFL, [], default_args, True)
    assert roster


def test_duo_constraint():
    default_args.duo = 'NE'
    roster = run(POSITIONS[NFL], NFL, [], default_args, True)
    team_instances = Counter([p.team for p in roster.players]).values()
    assert 2 in team_instances


def test_teams_constraint():
    default_args.teams = ['NE']
    roster = run(POSITIONS[NFL], NFL, [], default_args, True)
    for p in roster.players:
        if p.pos == 'DST':
            continue
        assert p.team == 'NE'


def test_banned_constraint():
    jg = 'Jimmy Garoppolo'
    default_args.teams = ['NE']
    default_args.banned = [jg]
    roster = run(POSITIONS[NFL], NFL, [], default_args, True)
    assert jg not in [p.name for p in roster.players]


def test_bad_constraints():
    default_args.lp = 1000
    roster = run(POSITIONS[NFL], NFL, [], default_args, True)
    assert roster is None
