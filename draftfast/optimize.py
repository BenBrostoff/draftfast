'''
A huge thanks to @swanson
this solution is based off
https://github.com/swanson/degenerate
'''

import random
from draftfast import player_pool as pool
from draftfast.orm import RosterSelect
from draftfast.optimizer import Optimizer
from exposure import parse_exposure_file, check_exposure, \
    get_exposure_table, get_exposure_matrix


def run(rule_set,
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
        ).format(optimizer_settings, len(players))
    return None


def run_multi(
    args,
    exposure_limit_file,
    exposure_random_seed,
):
    exposure_bounds = None
    if exposure_limit_file:
        exposure_bounds = parse_exposure_file(exposure_limit_file)

    # set the random seed globally for random lineup exposure
    if exposure_random_seed:
        random.seed(exposure_random_seed)

    rosters = []
    for _ in range(0, int(args.i)):
        roster = run(args.league, args, rosters, exposure_bounds)

        if roster:
            rosters.append(roster)
        else:
            break

    exposure_diffs = {}

    if rosters:
        print(get_exposure_table(rosters, exposure_bounds))
        print()
        print(get_exposure_matrix(rosters))
        print()

        exposure_diffs = check_exposure(rosters, exposure_bounds)
        for n, d in exposure_diffs.items():
            if d < 0:
                print('{} is UNDER exposure by {} lineups'.format(n, d))
            else:
                print('{} is OVER exposure by {} lineups'.format(n, d))

    return rosters, exposure_diffs
