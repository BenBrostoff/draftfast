# A huge thanks to swanson
# this solution is almost wholly based off
# https://github.com/swanson/degenerate

import csv
import subprocess
from sys import exit
import argparse

from itertools import islice
from ortools.linear_solver import pywraplp

import dke_exceptions as dke
import constants as cons
from orm import RosterSelect, Player

parser = argparse.ArgumentParser()

fns = 'data/{}-salaries.csv'
fnp = 'data/{}-projections.csv'
fnu = 'data/{}-upload.csv'


for opt in cons.OPTIMIZE_COMMAND_LINE:
    parser.add_argument(opt[0], help=opt[1], default=opt[2])

args = parser.parse_args()


def run(position_distribution, league, remove, args, test_mode=False):
    csv_name = 'test' if test_mode else 'current'
    solver = pywraplp.Solver('FD',
                             pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    all_players = []

    with open(fns.format(csv_name), 'rb') as csvfile:
        csvdata = csv.DictReader(csvfile)

        for idx, row in enumerate(csvdata):
            if idx > 0:
                player = Player(row['Position'], row['Name'], row['Salary'],
                                matchup=row['GameInfo'])
                if args.l == 'NBA':
                    player.proj = float(row['AvgPointsPerGame'])
                    player.team = row['teamAbbrev']
                all_players.append(player)

    if league == 'NFL':
        with open(fnp.format(csv_name), 'rb') as csvfile:
            csvdata = csv.DictReader(csvfile)
            mass_hold = [['playername', 'points', 'cost', 'ppd']]

            for row in csvdata:
                player = filter(lambda x: x.name in row['playername'],
                                all_players)
                if len(player) == 0:
                    continue

                player[0].proj = float(row['points'])
                player[0].marked = 'Y'
                player[0].team = row['playername'].split(' ')[-2]
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
        lambda x: x.name not in remove and
        (x.proj >= int(args.lp) or x.pos in ['DST', 'TE']) and
        x.cost <= int(args.ms) and
        x.team is not None,
        all_players)

    variables, solution = run_solver(solver,
                                     all_players,
                                     position_distribution)

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


def run_solver(solver, all_players, max_flex):
    '''
    Set objective and constraints, then optimize
    '''
    variables = []

    for player in all_players:
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
                if team == player.team and \
                           player.pos != 'QB':
                    team_cap.SetCoefficient(variables[i], 1)

    # force QB / WR or QB / TE combo on specified team
    if args.duo != 'n':
        if args.duo not in cons.ALL_NFL_TEAMS:
            raise dke.InvalidNFLTeamException(
                'You need to pass in a valid NFL team ' +
                'abbreviation to use this option. ' +
                'See valid team abbreviations here: '
                + str(cons.ALL_NFL_TEAMS))
        for pos, min_limit, max_limit in cons.DUO_TYPE[args.dtype.lower()]:
            position_cap = solver.Constraint(min_limit, max_limit)

            for i, player in enumerate(all_players):
                if pos == player.pos and \
                          player.team == args.duo:
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

    miss = len(filter(lambda x: x.marked != 'Y' and x.cost > min_cost,
                      all_players))

    if e_raise < miss:
        print 'Got {0} out of {1} total'.format(str(contained_report),
                                                str(total_report))
        raise dke.MissingPlayersException(
            'Total missing players at price point: ' + str(miss))


def create_upload_file_and_map_pids(pid_file, test_mode=False):
    # create upload file
    csv_name = 'test' if test_mode else 'current'
    with open(fnu.format(csv_name), "w") as f:
        writer = csv.writer(f)
        writer.writerow(
            ['QB', 'RB', 'RB', 'WR', 'WR', 'WR', 'TE', 'FLEX', 'DST'])

    # create a player map from name/position to id
    player_map = {}
    with open(pid_file, "r") as f:
        n = 0
        fields = None
        for line in f.readlines():
            n += 1
            if 'TeamAbbrev' in line:  # line with field names was found
                fields = line.split(',')
                break

        if not fields:
            raise dke.InvalidCSVUploadFileException(
                "Check that you're using the DK CSV upload template, " +
                "which can be found at " +
                "https://www.draftkings.com/lineup/upload.")

        f.close()
        f = islice(open(pid_file, "r"), n, None)
        reader = csv.DictReader(f, fieldnames=fields)
        for line in reader:
            player_map[line[' Name'] + " " + line['Position']] = line[' ID']

    return player_map


def update_upload_csv(player_map, players, test_mode=False):
    csv_name = 'test' if test_mode else 'current'
    with open(fnu.format(csv_name), "a") as f:
        writer = csv.writer(f)
        player_ids = []
        flexid = -1
        rbs = 0
        wrs = 0

        for p in players:
            # For the players in the roster, get their id.
            # they are sorted when they are printed out,
            # so the order is good, except for the flex player
            p_id = player_map[p.name + " " + p.pos]

            #  keep track of the flex player and write them out after the TE
            if (p.pos == 'WR'):
                if (wrs == 3):
                    flexid = p_id
                    continue
                wrs += 1
                player_ids.append(p_id)
            elif (p.pos == 'RB'):
                if (rbs == 2):
                    flexid = p_id
                    continue
                rbs += 1
                player_ids.append(p_id)
            elif (p.pos == 'TE'):
                player_ids.append(p_id)
                player_ids.append(flexid)
            else:
                player_ids.append(p_id)
        writer.writerow(player_ids)

if __name__ == "__main__":
    if args.pids:
        player_map = create_upload_file_and_map_pids(args.pids)
    if args.s == 'y' and args.l == 'NFL':
        subprocess.call(['python', 'scraper.py', args.w])

    rosters, remove = [], []
    for x in xrange(0, int(args.i)):
        rosters.append(run(cons.POSITIONS[args.l], args.l, remove, args))
        if args.pids:
            update_upload_csv(player_map, rosters[x].sorted_players()[:])
        if None not in rosters:
            for roster in rosters:
                for player in roster.players:
                    remove.append(player.name)
        else:
            exit()

    if args.pids and len(rosters) > 0:
        print "{} rosters now available for upload in file {}." \
               .format(len(rosters), fnu.format('current'))
