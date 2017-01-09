from optimize import run
from argparse import Namespace
from collections import Counter
from orm import NFLRoster, Player
from constants import POSITIONS

NFL = 'NFL'
default_args_dict = dict(
    dtype='wr',
    duo='n',
    i=1,
    season=2016,
    w=1,
    historical='n',
    l='NFL',
    limit='n',
    lp=0,
    no_double_te='n',
    mp=100,
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
)
default_args = Namespace(**default_args_dict)

def test_default_constraints():
    roster = run(NFL, [], default_args)
    assert roster


def test_multi_position():
    multi_pos_args = Namespace(**default_args_dict)
    multi_pos_args.locked = ['Eli Manning']
    roster = run(NFL, [], multi_pos_args)
    assert roster

def test_is_home():
    default_args.home = True
    roster = run(NFL, [], default_args)
    for p in roster.players:
        assert p.is_home
    default_args.home = False


def test_within_avg():
    avg_test_val = 3
    default_args.v_avg = avg_test_val
    roster = run(NFL, [], default_args)
    for player in roster.players:
        assert abs(player.v_avg) < avg_test_val
    default_args.v_avg = 10000


def test_duo_constraint():
    default_args.duo = 'NE'
    roster = run(NFL, [], default_args)
    team_instances = Counter([p.team for p in roster.players]).values()
    assert 2 in team_instances


def test_teams_constraint():
    default_args.teams = ['NE', 'Dal']
    roster = run(NFL, [], default_args)
    for p in roster.players:
        if p.pos == 'DST':
            continue
        assert p.team == 'NE' or p.team == 'Dal'


def test_banned_constraint():
    jg = 'Jimmy Garoppolo'
    default_args.teams = ['NE', 'Dal']
    default_args.banned = [jg]
    roster = run(NFL, [], default_args)
    assert jg not in [p.name for p in roster.players]


def test_locked_constraint():
    jb = 'Jacoby Brissett'
    default_args.teams = ['NE', 'Dal']
    default_args.banned = []
    default_args.locked = [jb]
    roster = run(NFL, [], default_args)
    assert [p for p in roster.players if p.name == jb][0].lock


def test_bad_constraints():
    default_args.lp = 1000
    roster = run(NFL, [], default_args)
    assert roster is None


def test_same_roster():
    roster_one = NFLRoster()
    roster_two = NFLRoster()
    for pos in POSITIONS['NFL']:
        for x in range(0, pos[1]):
            roster_one.add_player(Player(pos[0], 'Kacper{}'.format(x), 4000))
            roster_two.add_player(Player(pos[0], 'Kacper{}'.format(x), 4000))
    roster_one.add_player(Player('WR', 'Kacper8'.format(x), 4000))
    roster_two.add_player(Player('WR', 'Kacper8'.format(x), 4000))
    assert roster_one == roster_two
    roster_one.players.pop()
    assert not roster_one == roster_two
    roster_one.players.append(Player('WR', 'Kacper8'.format(x), 6000))
    assert not roster_one == roster_two
