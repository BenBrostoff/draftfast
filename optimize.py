'''
A huge thanks to @swanson
this solution is based off
https://github.com/swanson/degenerate
'''

import csv
import random
from sys import exit

from ortools.linear_solver import pywraplp

import constants as cons
import dke_exceptions as dke
import query_constraints as qc
import scrapers
from command_line import get_args
from csv_upload import nfl_upload, nba_upload
from orm import RosterSelect, Player, retrieve_all_players_from_history

_YES = 'y'
_DK_AVG = 'DK_AVG'


def run(league, remove, args):
    solver = pywraplp.Solver(
        'FD',
        pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING
    )

    all_players = retrieve_players(args, remove)

    flex_args = {}
    if args.no_double_te == _YES:
        flex_args['te_upper'] = 1
    if args.flex_position == 'RB':
        flex_args['rb_min'] = 3
    if args.flex_position == 'WR':
        flex_args['wr_min'] = 4

    cons.POSITIONS['NFL'] = cons.get_nfl_positions(**flex_args)

    variables, solution = run_solver(
        solver,
        all_players,
        args
    )

    if solution == solver.OPTIMAL:
        roster = RosterSelect().roster_gen(args.league)
        if args.source != _DK_AVG or args.proj:
            roster.projection_source = \
                scrapers.scrape_dict[args.source]['readable']

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


def retrieve_players(args, remove):
    if args.historical_date:
        all_players = retrieve_all_players_from_history(args)
    else:
        all_players = []
        with open(args.salary_file, 'rb') as csv_file:
            csv_data = csv.DictReader(csv_file)

            def generate_player(pos, row):
                avg = float(row.get('AvgPointsPerGame', 0))
                player = Player(
                    pos,
                    row['Name'],
                    row['Salary'],
                    possible_positions=row['Position'],
                    multi_position=('/' in row['Position']),
                    team=row['teamAbbrev'],
                    matchup=row['GameInfo'],
                    average_score=avg,
                    lock=(args.locked and row['Name'] in args.locked)
                )
                if args.source == _DK_AVG:
                    player.proj = avg

                return player

            for row in csv_data:
                for pos in row['Position'].split('/'):
                    all_players.append(generate_player(pos, row))

    _set_historical_points(all_players, args)
    _set_player_ownership(all_players, args)

    if args.source != _DK_AVG:
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
                matching_players = filter(name_match(row), all_players)

                if len(matching_players) == 0:
                    continue

                for p in matching_players:
                    p.proj = float(row['points'])
                    p.marked = 'Y'

    if not args.historical_date:
        _check_missing_players(all_players, args.sp, args.mp)

    # filter based on criteria and previously optimized
    # do not include DST or TE projections in min point threshold.
    return filter(
        qc.add_constraints(args, remove),
        all_players
    )


def run_solver(solver, all_players, args):
    '''
    Set objective and constraints, then optimize
    '''
    variables = []

    for player in all_players:
        if player.lock and not player.multi_position:
            variables.append(solver.IntVar(1, 1, player.solver_id))
        else:
            variables.append(solver.IntVar(0, 1, player.solver_id))

    objective = solver.Objective()
    objective.SetMaximization()

    # optimize on projected points
    for i, player in enumerate(all_players):
        objective.SetCoefficient(variables[i], player.proj)

    # set multi-player constraint
    multi_caps = {}
    for i, p in enumerate(all_players):
        if not p.multi_position:
            continue

        if p.name not in multi_caps:
            if p.lock:
                multi_caps[p.name] = solver.Constraint(1, 1)
            else:
                multi_caps[p.name] = solver.Constraint(0, 1)
        multi_caps[p.name].SetCoefficient(variables[i], 1)

    # set salary cap constraint
    salary_cap = solver.Constraint(0, cons.SALARY_CAP)
    for i, player in enumerate(all_players):
        salary_cap.SetCoefficient(variables[i], player.cost)

    # set roster size constraint
    size_cap = solver.Constraint(cons.ROSTER_SIZE[args.league],
                                 cons.ROSTER_SIZE[args.league])
    for variable in variables:
        size_cap.SetCoefficient(variable, 1)

    # set position limit constraint
    for position, min_limit, max_limit in cons.POSITIONS[args.league]:
        position_cap = solver.Constraint(min_limit, max_limit)

        for i, player in enumerate(all_players):
            if position == player.pos:
                position_cap.SetCoefficient(variables[i], 1)

    # set G / F NBA position limits
    if args.league in ['NBA', 'WNBA']:
        general_positions = {
            'NBA': cons.NBA_GENERAL_POSITIONS,
            'WNBA': cons.WNBA_GENERAL_POSITIONS,
        }[args.league]
        for general_position, min_limit, max_limit in \
                general_positions:
            position_cap = solver.Constraint(min_limit, max_limit)

            for i, player in enumerate(all_players):
                if general_position == player.nba_general_position:
                    position_cap.SetCoefficient(variables[i], 1)

    # max out at one player per team (allow QB combos)
    team_limits = set([(p.team, 0, 1) for p in all_players])
    if args.limit != 'n':
        for team, min_limit, max_limit in team_limits:
            team_cap = solver.Constraint(min_limit, max_limit)

            for i, player in enumerate(all_players):
                if team.upper() == player.team.upper() and \
                        player.pos != 'QB':
                    team_cap.SetCoefficient(variables[i], 1)

    # force QB / WR or QB / TE combo on specified team
    if args.duo != 'n':
        all_teams = set(p.team for p in all_players)
        if args.duo.upper() not in all_teams:
            raise dke.InvalidNFLTeamException(
                'You need to pass in a valid NFL team ' +
                'abbreviation to use this option. ' +
                'See valid team abbreviations here: '
                + str(all_teams)
            )
        for pos, min_limit, max_limit in cons.DUO_TYPE[args.dtype.lower()]:
            position_cap = solver.Constraint(min_limit, max_limit)

            for i, player in enumerate(all_players):
                if pos == player.pos and \
                          player.team.upper() == args.duo.upper():
                    position_cap.SetCoefficient(variables[i], 1)

    return variables, solver.Solve()


def _set_historical_points(all_players, args):
    if args.w and args.season and args.historical == _YES:
        print('Fetching {} season data for all players...'.format(args.season))
        for p in all_players:
            p.set_historical(int(args.w), int(args.season))


def _set_player_ownership(all_players, args):
    if args.po_location and args.po:
        with open(args.po_location, 'rb') as csv_file:
            csv_data = csv.DictReader(csv_file)
            for row in csv_data:
                player = filter(
                    lambda p: p.name in row['Name'],
                    all_players
                )
                if player:
                    player[0].projected_ownership_pct = float(row['%'])


_MISSING_ERROR = """
Got {} projections out of {} total players.

You are allowing {} players to be missing from your
projections compared to the total players DraftKings
will allow you to play. You can change this allowance
via the mp flag.
"""


def _check_missing_players(all_players, min_cost, e_raise):
    '''
    Check for significant missing players
    as names from different data do not match up
    continues or stops based on inputs
    '''
    contained_report = len(filter(lambda x: x.marked == 'Y', all_players))
    total_report = len(all_players)

    missing = filter(lambda x: x.marked != 'Y' and x.cost > min_cost,
                     all_players)
    miss_len = len(missing)
    if int(e_raise) < miss_len:
        print(_MISSING_ERROR) \
            .format(str(contained_report), str(total_report), e_raise)
        raise dke.MissingPlayersException(
            'Total missing players at price point: ' + str(miss_len))


def _randomize_projections(weight):
    '''
    Iterate through projections and multiply by a factor
    between (1-x) and (1+x).

    This can occasionally be useful for breaking patterns where a certain
    value group of players always show up in lineup results and you do not
    want to ban any of them, or to just see how slight changes in projections
    can impact optimization.
    '''
    hold = []
    proj_file = 'data/current-projections.csv'
    with open(proj_file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            hold.append(row)

    with open(proj_file, 'w') as csvfile:
        fieldnames = ['playername', 'points']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in hold:
            factor = 1 + random.uniform(-float(weight), float(weight))
            row['points'] = float(row['points']) * factor
            writer.writerow(row)

    print('Rewrite complete with weighted factor {}'.format(weight))


def check_validity(args):
    if args.s != _YES:
        with open(args.projection_file, 'rb') as csvfile:
            csvdata = csv.DictReader(csvfile)
            fieldnames = csvdata.fieldnames
            errors = []
            for f in ['playername', 'points']:
                if f not in fieldnames:
                    errors.append(f)

            if len(errors) > 0:
                raise Exception(
                    '''
                    If you are choosing to provide your own projection source,
                    you must provide the following fields: {}
                    '''.format(errors)
                )


if __name__ == '__main__':
    args = get_args()
    check_validity(args)

    uploader = nba_upload if args.league == 'NBA' else nfl_upload
    if not args.keep_pids:
        uploader.create_upload_file()
    if args.pids:
        player_map = uploader.map_pids(args.pids)
    if args.s == _YES and args.source != 'DK_AVG':
        try:
            scrapers.scrape(args.source)
            if args.randomize_projections:
                _randomize_projections(args.randomize_projections)
        except KeyError:
            raise dke.InvalidProjectionSourceException(
                'You must choose from the following data sources {}.'
                .format(scrapers.scrape_dict.keys()))

    rosters, remove = [], []
    for x in range(0, int(args.i)):
        rosters.append(run(args.league, remove, args))
        if args.pids:
            uploader.update_upload_csv(
                player_map, rosters[x].sorted_players()[:])
        if None not in rosters:
            for roster in rosters:
                for player in roster.players:
                    remove.append(player.name)
        else:
            exit()

    if args.pids and len(rosters) > 0:
        print(
            '{} rosters now available for upload in file {}.'
            .format(len(rosters), uploader.upload_file)
        )
