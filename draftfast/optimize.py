import random
from copy import deepcopy
from typing import List
from draftfast import player_pool as pool
from draftfast.orm import RosterSelect, Roster
from draftfast.optimizer import Optimizer
from draftfast.exposure import check_exposure, \
    get_exposure_table, get_exposure_matrix, get_exposure_args
from draftfast.rules import RuleSet
from draftfast.settings import PlayerPoolSettings, OptimizerSettings
from draftfast.lineup_constraints import LineupConstraints


def run(rule_set: RuleSet,
        player_pool: list,
        constraints: LineupConstraints = LineupConstraints(),
        optimizer_settings: OptimizerSettings = OptimizerSettings(),
        player_settings: PlayerPoolSettings = PlayerPoolSettings(),
        exposure_dict: dict = dict(),
        roster_gen: Roster = None,
        verbose=False) -> Roster:
    players = player_pool
    if player_settings.exist() or constraints.exist():
        players = pool.filter_pool(
            deepcopy(player_pool),
            player_settings,
        )

    if not isinstance(rule_set, RuleSet):
        raise Exception("RuleSet not defined. Please refer to the docs")

    if rule_set.game_type == 'showdown':
        if optimizer_settings.no_offense_against_defense:
            print('WARNING:')
            print('no_offense_against_defense setting ignored for showdown')
            print('game types. Use no_defense_against_captain instead.')
            print()

    optimizer = Optimizer(
        players=players,
        rule_set=rule_set,
        settings=optimizer_settings,
        lineup_constraints=constraints,
        exposure_dict=exposure_dict,
    )

    variables = optimizer.variables

    if optimizer.solve():
        if roster_gen:
            roster = roster_gen()
        else:
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
No solution found.
Try adjusting your query by taking away constraints.

OPTIMIZER CONSTRAINTS:

{}

LINEUP CONSTRAINTS:

{}

PLAYER POOL SETTINGS:

{}

PLAYER COUNT: {}
        '''.format(
                optimizer_settings,
                constraints,
                player_settings,
                len(players or [])
            )
        )
    return None


def run_multi(
    iterations: int,
    rule_set: RuleSet,
    player_pool: list,
    constraints: LineupConstraints = LineupConstraints(),
    player_settings: PlayerPoolSettings = PlayerPoolSettings(),
    optimizer_settings: OptimizerSettings = OptimizerSettings(),
    verbose=False,
    exposure_bounds: List[dict] = list(),
    exposure_random_seed=None,
) -> [List[Roster], list]:

    if not isinstance(rule_set, RuleSet):
        raise Exception("RuleSet not defined. Please refer to the docs")

    # set the random seed globally for random lineup exposure
    random.seed(exposure_random_seed)

    rosters = []
    for _ in range(0, iterations):
        exposure_dict = get_exposure_args(
            existing_rosters=optimizer_settings.existing_rosters,
            exposure_bounds=exposure_bounds,
            n=iterations,
            use_random=bool(exposure_random_seed),
            random_seed=exposure_random_seed,
        )

        roster = run(
            rule_set=rule_set,
            player_pool=player_pool,
            optimizer_settings=optimizer_settings,
            player_settings=player_settings,
            exposure_dict=exposure_dict,
            constraints=constraints,
            verbose=verbose,
        )
        if roster:
            optimizer_settings.existing_rosters += [roster]

        if roster:
            rosters.append(roster)
        else:
            break

        # clear ban/lock to reset exposure between iterations
        reset_player_ban_lock(player_pool)

    exposure_diffs = {}

    if rosters and verbose:
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


def reset_player_ban_lock(player_pool):
    for p in player_pool:
        p.ban = False
        p.lock = False
