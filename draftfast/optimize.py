'''
A huge thanks to @swanson
this solution is based off
https://github.com/swanson/degenerate
'''

import csv
import random
from draftfast import rules as cons, dke_exceptions as dke, player_pool as pool
from draftfast.command_line import get_args
from draftfast.csv_parse import nfl_upload, mlb_upload, nba_upload, salary_download
from draftfast.orm import RosterSelect, retrieve_all_players_from_history
from draftfast.optimizer import Optimizer
from draftfast.command_line import get_args
from exposure import parse_exposure_file, get_exposure_args, check_exposure, \
    get_exposure_table


_YES = 'y'
_DK_AVG = 'DK_AVG'

_GAMES = [
    'draftkings',
    'fanduel',
    cons.DRAFT_KINGS,
    cons.FAN_DUEL
]

# WIP - convert once structure in place


def beta_run(rule_set,
             player_pool,
             optimizer_settings=None,
             player_settings=None,
             upload_settings=None,
             verbose=False):
    players = pool.filter_pool(
        player_pool,
        player_settings,
    )
    optimizer = Optimizer(
        players=players,
        rule_set=rule_set,
        settings=optimizer_settings,
    )

    variables = optimizer.variables

    if optimizer.solve():
        roster = RosterSelect().roster_gen(rule_set.league)

        for i, player in enumerate(players):
            if variables[i].solution_value() == 1:
                roster.add_player(player)

        if verbose:
            print('Optimal roster for: {}'.format(rule_set.league))
            print(roster)

        return roster

    if verbose:
        print(
            '''
            No solution found for command line query.
            Try adjusting your query by taking away constraints.

            Active constraints: {}
            Player count: {}
            '''
        ).format(1, len(players))  # TODO - add better debugging
    return None


# TODO cleanup interfaces between run() and run_multi()
def run(league, args, existing_rosters=None, exposure_bounds=None):
    if exposure_bounds:
        exposure_args = get_exposure_args(
            existing_rosters=existing_rosters,
            exposure_bounds=exposure_bounds,
            n=int(args.i),
            use_random=args.random_exposure,
            random_seed=args.__dict__.get('random_exposure_seed', 0)
        )

        args.locked = exposure_args['locked']
        args.banned = exposure_args['banned']

    args.game = _get_game(args)

    # this is where player filtering is done for banned/locked/home
    all_players = retrieve_players(args)

    salary_max = _get_salary(args)
    salary_min = 0
    roster_size = _get_roster_size(args)
    position_limits = _get_position_limits(args)
    general_position_limits = _get_general_position_limits(args)

    optimizer = Optimizer(
        players=all_players,
        existing_rosters=existing_rosters,
        settings=args,
        salary_min=salary_min,
        salary_max=salary_max,
        roster_size=roster_size,
        position_limits=position_limits,
        general_position_limits=general_position_limits,
    )
    variables = optimizer.variables

    opt_message = 'Optimized over {} players'.format(len(all_players))
    print('\x1b[0;32;40m{}\x1b[0m'.format(opt_message))

    if optimizer.solve():
        roster = RosterSelect().roster_gen(args.league)

        for i, player in enumerate(all_players):
            if variables[i].solution_value() == 1:
                roster.add_player(player)

        print('Optimal roster for: {}'.format(league))
        print(roster)
        print()

        return roster
    else:
        print(
            '''
            No solution found for command line query.
            Try adjusting your query by taking away constraints.
            '''
        )
        return None


def run_multi(args):
    exposure_bounds = None
    exposure_limit_file = args.__dict__.get('exposure_limit_file')
    if exposure_limit_file:
        exposure_bounds = parse_exposure_file(exposure_limit_file)

    # set the random seed globally for random lineup exposure
    random.seed(args.__dict__.get('exposure_random_seed'))

    rosters = []
    for _ in range(0, int(args.i)):
        roster = run(args.league, args, rosters, exposure_bounds)

        if roster:
            rosters.append(roster)
            if args.pids:
                uploader.update_upload_csv(
                    player_map, roster
                )
        else:
            break

    exposure_diffs = {}

    if rosters:
        print(get_exposure_table(rosters, exposure_bounds))
        print()

        exposure_diffs = check_exposure(rosters, exposure_bounds)
        for n, d in exposure_diffs.items():
            if d < 0:
                print('{} is UNDER exposure by {} lineups'.format(n, d))
            else:
                print('{} is OVER exposure by {} lineups'.format(n, d))

    return rosters, exposure_diffs


def retrieve_players(args):
    if args.historical_date:
        all_players = retrieve_all_players_from_history(args)
    else:
        all_players = []
        with open(args.salary_file, 'r') as csv_file:
            csv_data = csv.DictReader(csv_file)

            for row in csv_data:
                for pos in row['Position'].split('/'):
                    all_players.append(salary_download.generate_player(
                        pos, row, args
                    ))

    if args.__dict__.get('use_average'):
        for p in all_players:
            p.proj = p.average_score
            p.marked = True
    elif args.salary_file and args.projection_file:
        with open(args.projection_file, 'r') as csvfile:
            csvdata = csv.DictReader(csvfile)

            # hack for weird defensive formatting
            def name_match(row):
                def match_fn(p):
                    if p.pos == 'DST':
                        return p.name.strip() in row['playername']
                    return p.name in row['playername']
                return match_fn

            for row in csvdata:
                matching_players = list(filter(name_match(row), all_players))

                if len(matching_players) == 0:
                    continue

                for p in matching_players:
                    p.proj = float(row['points'])
                    p.marked = True

    if not args.historical_date:
        _check_missing_players(all_players, args.mp)

    # filter based on criteria and previously optimized
    # do not include DST or TE projections in min point threshold.
    return list(filter(
        qc.add_constraints(args),
        all_players
    ))
