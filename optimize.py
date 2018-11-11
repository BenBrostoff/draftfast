'''
A huge thanks to @swanson
this solution is based off
https://github.com/swanson/degenerate
'''

import csv
from sys import exit
import constants as cons
import dke_exceptions as dke
import query_constraints as qc
from command_line import get_args
from csv_parse import nfl_upload, nba_upload, mlb_upload
from orm import RosterSelect, retrieve_all_players_from_history
from csv_parse.salary_download import generate_player
from optimizer import Optimizer

_YES = 'y'
_DK_AVG = 'DK_AVG'

_GAMES = [
    'draftkings',
    'fanduel',
    cons.DRAFT_KINGS,
    cons.FAN_DUEL
]


def run(league, args, existing_rosters=None):
    args.game = _get_game(args)
    all_players = retrieve_players(args)
    salary = _get_salary(args)
    roster_size = _get_roster_size(args)
    position_limits = _get_position_limits(args)
    general_position_limits = _get_general_position_limits(args)

    optimizer = Optimizer(
        players=all_players,
        existing_rosters=existing_rosters,
        settings=args,
        salary=salary,
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

        return roster
    else:
        print(
            '''
            No solution found for command line query.
            Try adjusting your query by taking away constraints.
            '''
        )
        return None


def retrieve_players(args):
    if args.historical_date:
        all_players = retrieve_all_players_from_history(args)
    else:
        all_players = []
        with open(args.salary_file, 'rb') as csv_file:
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
        with open(args.projection_file, 'rb') as csvfile:
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


def _set_player_ownership(all_players, args):
    if args.po_location and args.po:
        with open(args.po_location, 'rb') as csv_file:
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
        print(dke.MISSING_ERROR) \
            .format(str(contained_report), str(total_report), e_raise)
        raise dke.MissingPlayersException(
            'Total missing players at price point: ' + str(miss_len))


def check_validity(args):
    if args.projection_file:
        with open(args.projection_file, 'rb') as csvfile:
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

    if not args.keep_pids:
        uploader.create_upload_file()
    if args.pids:
        player_map = uploader.map_pids(args.pids)

    rosters = []
    for _ in range(0, int(args.i)):
        roster = run(args.league, args, rosters)

        if roster:
            rosters.append(roster)
            if args.pids:
                uploader.update_upload_csv(
                    player_map, roster
                )
        else:
            exit()

    if args.pids and len(rosters) > 0:
        print(
            '{} rosters now available for upload in file {}.'
            .format(len(rosters), uploader.upload_file)
        )
