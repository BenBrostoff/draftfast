# import os
# from nose import tools as ntools
# from draftfast.optimize import run, run_multi
# from argparse import Namespace
#
# CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
#
# NFL = 'NFL'
# args_dict = dict(
#     game='draftkings',
#     i=1,
#     season=2016,
#     w=1,
#     league='NFL',
#     limit='n',
#     lp=0,
#     no_double_te='n',
#     mp=300,
#     ms=10000,
#     s='n',
#     sp=3000,
#     home=None,
#     locked=None,
#     teams=None,
#     banned=None,
#     po=0,
#     po_location=None,
#     v_avg=10000,
#     test_mode=True,
#     salary_file='{}/data/test-salaries.csv'.format(CURRENT_DIR),
#     projection_file='{}/data/test-projections.csv'.format(CURRENT_DIR),
#     flex_position=None,
#     min_avg=-1,
#     historical_date=None,
#     pids=None,
#     random_exposure='n',
# )
#
#
# def test_within_avg():
#     args = Namespace(**args_dict)
#     avg_test_val = 3
#     args.v_avg = avg_test_val
#     roster = run(NFL, args)
#     for player in roster.players:
#         ntools.assert_less(abs(player.v_avg), avg_test_val)
#
#
# def test_teams_constraint():
#     args = Namespace(**args_dict)
#     args.teams = ['NE', 'Dal']
#     roster = run(NFL, args)
#     for p in roster.players:
#         if p.pos == 'DST':
#             continue
#         ntools.assert_true(p.team == 'NE' or p.team == 'Dal')
