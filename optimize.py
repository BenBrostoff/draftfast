'''
A huge thanks to @swanson
this solution is based off
https://github.com/swanson/degenerate
'''

import csv
import constants as cons
import dke_exceptions as dke
import query_constraints as qc
from command_line import get_args
from csv_parse import nfl_upload, nba_upload, mlb_upload
from orm import RosterSelect, retrieve_all_players_from_history
from csv_parse.salary_download import generate_player
from exposure import parse_exposure_file, get_exposure_args, check_exposure, \
                     get_exposure_table
from optimizer import Optimizer
import random

_YES = 'y'
_DK_AVG = 'DK_AVG'

_GAMES = [
    'draftkings',
    'fanduel',
    cons.DRAFT_KINGS,
    cons.FAN_DUEL
]


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
        locked = args.locked + exposure_args['locked']
        banned = args.banned + exposure_args['banned']

    player_groups = _get_player_groups(args)
    if player_groups:
        locked += player_groups.get_locked()
        locked += player_groups.get_locked()

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
        player_groups=player_groups,
        locked=locked,
        banned=banned,
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
                    all_players.append(generate_player(
                        pos, row, args
                    ))

    _set_player_ownership(all_players, args)

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


def _get_game(settings):
    if settings.game not in _GAMES:
        raise Exception(
            'You chose {} as DFS game. Available options are {}'
            .format(settings.game, _GAMES)
        )

    game = cons.DRAFT_KINGS \
        if settings.game == 'draftkings' or settings.game == cons.DRAFT_KINGS \
        else cons.FAN_DUEL

    return game


def _get_salary(settings):
    return cons.SALARY_CAP[settings.league][settings.game]


def _get_roster_size(settings):
    return cons.ROSTER_SIZE[settings.game][settings.league]


def _get_position_limits(settings):
    if settings.league == 'NFL':
        flex_args = {}
        if settings.no_double_te == _YES:
            flex_args['te_upper'] = 1
        if settings.flex_position == 'RB':
            flex_args['rb_min'] = 3
        if settings.flex_position == 'WR':
            flex_args['wr_min'] = 4

        cons.POSITIONS[settings.game]['NFL'] = \
            cons.get_nfl_positions(**flex_args)

    return cons.POSITIONS[settings.game][settings.league]


def _get_general_position_limits(settings):
    if settings.league in ['NBA', 'WNBA']:
        return {
            'NBA': cons.NBA_GENERAL_POSITIONS,
            'WNBA': cons.WNBA_GENERAL_POSITIONS,
        }[settings.league]

    return []


def _get_player_groups(settings):
    f = settings.__dict__.get('groups_file')
    if f:
        return PlayerGroups(f)

    return None


def _set_player_ownership(all_players, args):
    if args.po_location and args.po:
        with open(args.po_location, 'r') as csv_file:
            csv_data = csv.DictReader(csv_file)
            for row in csv_data:
                player = [p for p in all_players if p.name in row['Name']]
                if player:
                    player[0].projected_ownership_pct = float(row['%'])


def _check_missing_players(all_players, e_raise):
    '''
    Check for significant missing players
    as names from different data do not match up
    continues or stops based on inputs
    '''
    contained_report = len([x for x in all_players if x.marked])
    total_report = len(all_players)

    missing = [x for x in all_players if not x.marked]
    miss_len = len(missing)

    if int(e_raise) < miss_len:
        print(dke.MISSING_ERROR
              .format(str(contained_report), str(total_report), e_raise))
        raise dke.MissingPlayersException(
            'Total missing players at price point: ' + str(miss_len))


def check_validity(args):
    if args.projection_file:
        with open(args.projection_file, 'r') as csvfile:
            csvdata = csv.DictReader(csvfile)
            fieldnames = csvdata.fieldnames
            errors = []
            for f in ['playername', 'points']:
                if f not in fieldnames:
                    errors.append(f)

            if len(errors) > 0:
                raise Exception(dke.CSV_ERROR.format(errors))


if __name__ == '__main__':
    args = get_args()
    check_validity(args)

    uploader = None
    if args.league == 'NBA':
        uploader = nba_upload
    elif args.league == 'MLB':
        uploader = mlb_upload
    else:
        uploader = nfl_upload

    player_map = None
    if not args.keep_pids:
        uploader.create_upload_file()
    if args.pids:
        player_map = uploader.map_pids(args.pids)

    rosters, _ = run_multi(args)

    if args.pids and len(rosters) > 0:
        print(
            '{} rosters now available for upload in file {}.'
            .format(len(rosters), uploader.upload_file)
        )
