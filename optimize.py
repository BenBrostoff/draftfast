# A huge thanks to swanson
# this solution is almost wholly based off
# https://github.com/swanson/degenerate
import os
import csv
from sys import exit

from ortools.linear_solver import pywraplp

import constants as cons
import dke_exceptions as dke
import query_constraints as qc
import scrapers
from command_line import get_args
from csv_upload import nfl_upload, nba_upload
from orm import RosterSelect, Player

_YES = 'y'


def run(league, remove, args):
    csv_name = [os.getcwd() + '/data', 'test'] if args.test_mode \
        else ['data', 'current']
    solver = pywraplp.Solver('FD',
                             pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    all_players = []

    with open(args.salary_file, 'rb') as csvfile:
        csvdata = csv.DictReader(csvfile)

        def generate_player(pos, row):
            return Player(
                pos,
                row['Name'],
                row['Salary'],
                possible_positions=row['Position'],
                multi_position=('/' in row['Position']),
                team=row['teamAbbrev'],
                matchup=row['GameInfo'],
                average_score=float(
                    row.get('AvgPointsPerGame', 0)),
                lock=(args.locked and row['Name'] in args.locked))

        for row in csvdata:
            for pos in row['Position'].split('/'):
                all_players.append(
                    generate_player(pos, row)
                )

    if args.w and args.season and args.historical == _YES:
        print('Fetching {} season data for all players...'
              .format(args.season))
        for p in all_players:
            p.set_historical(int(args.w), int(args.season))

    if args.po_location and args.po:
        with open(args.po_location, 'rb') as csvfile:
            csvdata = csv.DictReader(csvfile)
            for row in csvdata:
                player = filter(
                    lambda p: p.name in row['Name'],
                    all_players)
                if player:
                    player[0].projected_ownership_pct = float(row['%'])

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

    _check_missing_players(all_players, args.sp, args.mp)

    # filter based on criteria and previously optimized
    # do not include DST or TE projections in min point threshold.
    all_players = filter(
        qc.add_constraints(args, remove),
        all_players)

    if args.no_double_te == _YES:
        cons.POSITIONS['NFL'] = cons.get_nfl_positions(te_upper=1)

    variables, solution = run_solver(solver,
                                     all_players,
                                     args)

    if solution == solver.OPTIMAL:
        roster = RosterSelect().roster_gen(args.l)
        roster.projection_source = \
            scrapers.scrape_dict[args.source]['readable']

        for i, player in enumerate(all_players):
            if variables[i].solution_value() == 1:
                roster.add_player(player)

        print "Optimal roster for: %s" % league
        print roster
        print

        return roster
    else:
        print("No solution found for command line query. " +
              "Try adjusting your query by taking away constraints.")
        return None


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
    size_cap = solver.Constraint(cons.ROSTER_SIZE[args.l],
                                 cons.ROSTER_SIZE[args.l])
    for variable in variables:
        size_cap.SetCoefficient(variable, 1)

    # set position limit constraint
    for position, min_limit, max_limit in cons.POSITIONS[args.l]:
        position_cap = solver.Constraint(min_limit, max_limit)

        for i, player in enumerate(all_players):
            if position == player.pos:
                position_cap.SetCoefficient(variables[i], 1)

    # set G / F NBA position limits
    if args.l == 'NBA':
        for general_position, min_limit, max_limit in \
                cons.NBA_GENERAL_POSITIONS:
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
                + str(all_teams))
        for pos, min_limit, max_limit in cons.DUO_TYPE[args.dtype.lower()]:
            position_cap = solver.Constraint(min_limit, max_limit)

            for i, player in enumerate(all_players):
                if pos == player.pos and \
                          player.team.upper() == args.duo.upper():
                    position_cap.SetCoefficient(variables[i], 1)

    return variables, solver.Solve()


def _check_missing_players(all_players, min_cost, e_raise):
    '''
    check for significant missing players
    as names from different data do not match up
    continues or stops based on inputs
    '''
    contained_report = len(filter(lambda x: x.marked == 'Y', all_players))
    total_report = len(all_players)

    missing = filter(lambda x: x.marked != 'Y' and x.cost > min_cost,
                     all_players)
    miss_len = len(missing)
    if e_raise < miss_len:
        print 'Got {0} out of {1} total'.format(str(contained_report),
                                                str(total_report))
        raise dke.MissingPlayersException(
            'Total missing players at price point: ' + str(miss_len))


if __name__ == "__main__":
    args = get_args()
    uploader = nba_upload if args.l == 'NBA' else nfl_upload
    if not args.keep_pids:
        uploader.create_upload_file()
    if args.pids:
        player_map = uploader.map_pids(args.pids)
    if args.s == _YES:
        try:
            scrapers.scrape(args.source)
        except KeyError:
            raise dke.InvalidProjectionSourceException(
                'You must choose from the following data sources {}.'
                .format(scrapers.scrape_dict.keys()))

    rosters, remove = [], []
    for x in xrange(0, int(args.i)):
        rosters.append(run(args.l, remove, args))
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
        print "{} rosters now available for upload in file {}." \
               .format(len(rosters), uploader.upload_file)
