import random
from typing import List
from draftfast import player_pool as pool
from draftfast.orm import RosterSelect, Roster
from draftfast.optimizer import Optimizer
from draftfast.exposure import check_exposure, \
    get_exposure_table, get_exposure_matrix
from draftfast.rules import RuleSet


def run(rule_set: RuleSet,
        player_pool: list,
        optimizer_settings=None,
        player_settings=None,
        verbose=False) -> Roster:
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
    iterations: int,
    rule_set: RuleSet,
    player_pool: list,
    optimizer_settings=None,
    player_settings=None,
    verbose=False,
    exposure_bounds=None,
    exposure_random_seed=None,
) -> List[Roster]:

    # set the random seed globally for random lineup exposure
    if exposure_random_seed:
        random.seed(exposure_random_seed)

    rosters = []
    for _ in range(0, iterations):
        roster = run(
            rule_set=rule_set,
            player_pool=player_pool,
            optimizer_settings=optimizer_settings,
            player_settings=player_settings,
            verbose=verbose,
        )

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
