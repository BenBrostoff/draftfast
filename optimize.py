# A huge thanks to swanson
# this solution is almost wholly based off
# https://github.com/swanson/degenerate

import csv
from sys import exit

from ortools.linear_solver import pywraplp

import scrapers
import upload
import query_constraints as qc
import dke_exceptions as dke
import constants as cons
from orm import RosterSelect, Player
from command_line import get_args

fns = 'data/{}-salaries.csv'
fnp = 'data/{}-projections.csv'
_YES = 'y'


def run(position_distribution, league, remove, args, test_mode=False):
    csv_name = 'test' if test_mode else 'current'
    solver = pywraplp.Solver('FD',
                             pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    all_players = []

    with open(fns.format(csv_name), 'rb') as csvfile:
        csvdata = csv.DictReader(csvfile)

        for row in csvdata:
            player = Player(row['Position'], row['Name'], row['Salary'],
                            team=row['teamAbbrev'],
                            matchup=row['GameInfo'],
                            lock=(args.locked and
                                  row['Name'] in args.locked))
            if args.l == 'NBA':
                player.proj = float(row['AvgPointsPerGame'])
                player.team = row['teamAbbrev']
            all_players.append(player)

    if args.w and args.season and args.historical == _YES:
        print('Fetching {} season data for all players...'
              .format(args.season))
        for p in all_players:
            p.set_historical(int(args.w), int(args.season))

    if league == 'NFL':
        if args.po_location and args.po:
            with open(args.po_location, 'rb') as csvfile:
                csvdata = csv.DictReader(csvfile)
                for row in csvdata:
                    player = filter(
                        lambda p: p.name in row['Name'],
                        all_players)
                    if player:
                        player[0].projected_ownership_pct = float(row['%'])

        with open(fnp.format(csv_name), 'rb') as csvfile:
            csvdata = csv.DictReader(csvfile)
            mass_hold = [['playername', 'points', 'cost', 'ppd']]

            # hack for weird defensive formatting
            def name_match(row):
                def match_fn(p):
                    if p.pos == 'DST':
                        return p.name.strip() in row['playername']
                    return p.name in row['playername']
                return match_fn

            for row in csvdata:
                player = filter(name_match(row), all_players)

                if len(player) == 0:
                    continue

                player[0].proj = float(row['points'])
                player[0].marked = 'Y'
                listify_holder = [
                    row['playername'],
                    row['points']
                ]
                if '0.0' not in row['points'] or player[0].cost != 0:
                    ppd = float(row['points']) / float(player[0].cost)
                else:
                    ppd = 0
                listify_holder.extend([player[0].cost,
                                       ppd * 100000])
                mass_hold.append(listify_holder)

        check = []
        with open(fns.format(csv_name), 'rb') as csvdata:
            for row in csvdata:
                check = row
                break

        with open(fnp.format(csv_name), 'wb') as csvdata:
            if len(check) == 4:
                pass
            else:
                writer = csv.writer(csvdata, lineterminator='\n')
                writer.writerows(mass_hold)

    if league == 'NFL':
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
                                     position_distribution,
                                     args)

    if solution == solver.OPTIMAL:
        roster = RosterSelect().roster_gen(args.l)

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


def run_solver(solver, all_players, max_flex, args):
    '''
    Set objective and constraints, then optimize
    '''
    variables = []

    for player in all_players:
        if player.lock:
            variables.append(solver.IntVar(1, 1, player.name))
        else:
            variables.append(solver.IntVar(0, 1, player.name))

    objective = solver.Objective()
    objective.SetMaximization()

    # optimize on projected points
    for i, player in enumerate(all_players):
        objective.SetCoefficient(variables[i], player.proj)

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

    # max out at one player per team (allow QB combos)
    if args.limit != 'n':
        for team, min_limit, max_limit in cons.COMBO_TEAM_LIMITS_NFL:
            team_cap = solver.Constraint(min_limit, max_limit)

            for i, player in enumerate(all_players):
                if team.upper() == player.team.upper() and \
                           player.pos != 'QB':
                    team_cap.SetCoefficient(variables[i], 1)

    # force QB / WR or QB / TE combo on specified team
    if args.duo != 'n':
        if args.duo.upper() not in cons.ALL_NFL_TEAMS:
            raise dke.InvalidNFLTeamException(
                'You need to pass in a valid NFL team ' +
                'abbreviation to use this option. ' +
                'See valid team abbreviations here: '
                + str(cons.ALL_NFL_TEAMS))
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
    if not args.keep_pids:
        upload.create_upload_file()
    if args.pids:
        player_map = upload.map_pids(args.pids)
    if args.s == _YES and args.l == 'NFL':
        try:
            scrapers.scrape(args.source)
        except KeyError:
            raise dke.InvalidProjectionSourceException(
                'You must choose from the following data sources {}.'
                .format(scrapers.scrape_dict.keys()))

    rosters, remove = [], []
    for x in xrange(0, int(args.i)):
        rosters.append(run(cons.POSITIONS[args.l], args.l, remove, args))
        if args.pids:
            upload.update_upload_csv(
                player_map, rosters[x].sorted_players()[:])
        if None not in rosters:
            for roster in rosters:
                for player in roster.players:
                    remove.append(player.name)
        else:
            exit()

    if args.pids and len(rosters) > 0:
        print "{} rosters now available for upload in file {}." \
               .format(len(rosters), upload.upload_file)
