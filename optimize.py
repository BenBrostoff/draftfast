# A huge thanks to swanson
# this solution is almost wholly based off
# https://github.com/swanson/degenerate

import csv
import subprocess
from sys import argv
import time
import argparse
from ortools.linear_solver import pywraplp

from orm import Player, Roster
from constants import *

parser = argparse.ArgumentParser()

for opt in OPTIMIZE_COMMAND_LINE:
    parser.add_argument(opt[0], help=opt[1], default=opt[2])

args = parser.parse_args()

def check_missing_players(all_players, min_cost, e_raise):
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
        raise Exception('Total missing players at price point: ' + str(miss))

def run_solver(solver, all_players, max_flex):
    '''
    handle or-tools logic
    '''
    variables = []

    for player in all_players:
        variables.append(solver.IntVar(0, 1, player.name))
      
    objective = solver.Objective()
    objective.SetMaximization()

    for i, player in enumerate(all_players):
        objective.SetCoefficient(variables[i], player.proj)

    salary_cap = solver.Constraint(0, SALARY_CAP)
    for i, player in enumerate(all_players):
        salary_cap.SetCoefficient(variables[i], player.cost)

    for position, limit in max_flex:
        position_cap = solver.Constraint(0, limit)

        for i, player in enumerate(all_players):
            if position == player.pos:
                position_cap.SetCoefficient(variables[i], 1)

    size_cap = solver.Constraint(ROSTER_SIZE, ROSTER_SIZE)
    for variable in variables:
        size_cap.SetCoefficient(variable, 1)

    return variables, solver.Solve()


def run(max_flex, maxed_over, remove):
    solver = pywraplp.Solver('FD', 
                             pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    all_players = []
    with open('data/dk-salaries-current-week.csv', 'rb') as csvfile:
        csvdata = csv.reader(csvfile, skipinitialspace=True)

        for idx, row in enumerate(csvdata):
            if idx > 0 and int(row[2]) <= int(args.ms):
                all_players.append(Player(row[0], row[1], row[2],
                                   matchup=row[3]))

    # give each a ranking
    all_players = sorted(all_players, key=lambda x: x.cost, reverse=True)
    for idx, x in enumerate(all_players):
        x.cost_ranking = idx + 1

    with open('data/fan-pros.csv', 'rb') as csvfile:
        csvdata = csv.DictReader(csvfile)
        mass_hold = [['playername', 'points', 'cost', 'ppd']]

        for row in csvdata:
            holder = row
            player = filter(lambda x: x.name in row['playername'], all_players)
            try:
                player[0].proj = int(int(row['points'].split('.')[0]))
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
            except Exception, e:
                print e

    check = []
    with open('data/fan-pros.csv', 'rb') as csvdata:
        for row in csvdata:
            check = row
            break

    with open('data/fan-pros.csv', 'wb') as csvdata:        
        if len(check) == 4:
            pass
        else:
            writer = csv.writer(csvdata, lineterminator='\n')
            writer.writerows(mass_hold)

    check_missing_players(all_players, args.sp, args.mp)


    # remove previously optimize
    all_players = filter(lambda x: x.name not in remove, all_players)

    variables, solution = run_solver(solver, all_players, max_flex)

    if solution == solver.OPTIMAL:
        roster = Roster()

        for i, player in enumerate(all_players):
            if variables[i].solution_value() == 1:
                roster.add_player(player)

        print "Optimal roster for: %s" % maxed_over
        print roster
        return roster
    else:
      raise Exception('No solution error')


if __name__ == "__main__":
    if args.scrape == 'y':
        subprocess.call(['python', 'scraper.py', args.w])
    rosters, remove = [], []
    for x in xrange(0, int(args.i)):
        for max_flex in ALL_LINEUPS.iterkeys():
            rosters.append(run(ALL_LINEUPS[max_flex], max_flex, remove))
        for roster in rosters:
            for player in roster.players:
                remove.append(player.name)
