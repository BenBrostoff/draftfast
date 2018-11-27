from nose import tools as ntools
from draftfast.optimize import beta_run
from draftfast import rules
from draftfast.orm import Player
from draftfast.settings import OptimizerSettings

mock_player_pool = [
    Player(name='A1', cost=5500, proj=55, pos='PG'),
    Player(name='A2', cost=5500, proj=55, pos='PG'),
    Player(name='A3', cost=5500, proj=55, pos='SG'),
    Player(name='A4', cost=5500, proj=55, pos='SG'),
    Player(name='A5', cost=5500, proj=55, pos='SF'),
    Player(name='A6', cost=5500, proj=55, pos='SF'),
    Player(name='A7', cost=5500, proj=55, pos='PF'),
    Player(name='A8', cost=5500, proj=55, pos='PF'),
    Player(name='A9', cost=5500, proj=55, pos='C'),
    Player(name='A10', cost=5500, proj=55, pos='C'),
]

def test_nba_dk():
    roster = beta_run(
        rule_set=rules.DK_NBA_RULE_SET,
        player_pool=mock_player_pool,
        verbose=True,
    )
    ntools.assert_not_equals(roster, None)


def test_nba_dk_with_csv():
    roster = beta_run(
        rule_set=rules.DK_NBA_RULE_SET,
        player_pool=mock_player_pool,
        verbose=True,
    )
    ntools.assert_not_equals(roster, None)


def test_nba_fd():
    roster = beta_run(
        rule_set=rules.FD_NBA_RULE_SET,
        player_pool=mock_player_pool,
    )
    ntools.assert_not_equals(roster, None)


def test_nfl_dk():
    roster = beta_run(
        rule_set=rules.DK_NFL_RULE_SET,
        player_pool=mock_player_pool,
    )
    ntools.assert_not_equals(roster, None)


def test_nfl_fd():
    roster = beta_run(
        rule_set=rules.FD_NFL_RULE_SET,
        player_pool=mock_player_pool,
    )
    ntools.assert_not_equals(roster, None)


# def test_multi_roster():
#     args = Namespace(**args_dict)
#     roster = run(NFL, args)
#     second_roster = run(NFL, args, [roster])
#     ntools.assert_not_equals(roster == second_roster, True)
#
#
# def test_stack():
#     args = Namespace(**args_dict)
#     args.stack = 'NE'
#     args.stack_count = 5
#     roster = run(NFL, args)
#     ne_players_count = len([
#         p for p in roster.sorted_players()
#         if p.team == 'NE'
#     ])
#     ntools.assert_equals(5, ne_players_count)
#
#
# def test_force_combo():
#     # no combo
#     args = Namespace(**args_dict)
#     roster = run(NFL, args)
#     qb = roster.sorted_players()[0]
#     ntools.assert_equal(qb.pos, 'QB')
#     team_count = len([
#         x for x in roster.sorted_players()
#         if x.team == qb.team
#     ])
#     ntools.assert_equals(team_count, 1)
#
#     # qb/wr combo
#     args = Namespace(**args_dict)
#     args.force_combo = True
#     roster = run(NFL, args)
#     qb = roster.sorted_players()[0]
#     ntools.assert_equal(qb.pos, 'QB')
#     team_count = len([
#         x for x in roster.sorted_players()
#         if x.team == qb.team
#     ])
#     ntools.assert_equals(team_count, 2)
#
#
# def test_te_combo():
#     # wr combo
#     args = Namespace(**args_dict)
#     args.force_combo = True
#     args.banned = ['Eli Manning']
#
#     roster = run(NFL, args)
#     qb = roster.sorted_players()[0]
#     ntools.assert_equal(qb.pos, 'QB')
#     team_count = len([
#         x for x in roster.sorted_players()
#         if x.team == qb.team
#     ])
#     ntools.assert_equals(team_count, 2)
#
#     # qb/te combo
#     args.combo_allow_te = True
#     roster = run(NFL, args)
#     qb = roster.sorted_players()[0]
#     ntools.assert_equal(qb.pos, 'QB')
#     team_count = len([
#         x for x in roster.sorted_players()
#         if x.team == qb.team and x.pos == 'TE'
#     ])
#     ntools.assert_equals(team_count, 1)
#
#
# def test_no_double_te():
#     args = Namespace(**args_dict)
#     args.locked = ['Rob Gronkowski']
#     roster = run(NFL, args)
#     qb = roster.sorted_players()[0]
#     ntools.assert_equal(qb.pos, 'QB')
#     te_count = len([
#         x for x in roster.sorted_players()
#         if x.pos == 'TE'
#     ])
#     ntools.assert_equals(te_count, 2)
#     args.no_double_te = 'y'
#     roster = run(NFL, args)
#     qb = roster.sorted_players()[0]
#     ntools.assert_equal(qb.pos, 'QB')
#     te_count = len([
#         x for x in roster.sorted_players()
#         if x.pos == 'TE'
#     ])
#     ntools.assert_equals(te_count, 1)
