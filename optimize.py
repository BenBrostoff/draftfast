# A huge thanks to swanson
# this solution is almost wholly based off
# https://github.com/swanson/degenerate

import csv
import subprocess
from sys import argv
from ortools.linear_solver import pywraplp
from orm import Player, Roster
from constants import *
import time

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


def run(max_flex, maxed_over):
    solver = pywraplp.Solver('FD', 
                             pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    all_players = []
    with open('data/dk-salaries-week-1.csv', 'rb') as csvfile:
        csvdata = csv.reader(csvfile, skipinitialspace=True)

        for idx, row in enumerate(csvdata):
            if idx > 0:
                all_players.append(Player(row[0], row[1], row[2]))

    # give each a ranking
    all_players = sorted(all_players, key=lambda x: x.cost, reverse=True)
    for idx, x in enumerate(all_players):
        x.cost_ranking = idx + 1

    with open('data/fan-pros.csv', 'rb') as csvfile:
        csvdata = csv.DictReader(csvfile)
        worked = 0

        for row in csvdata:
            player = filter(lambda x: x.name in row['playername'], all_players)
            try:
                player[0].proj = int(int(row['points'].split('.')[0]))
                player[0].marked = 'Y'
            except:
                pass

    check_missing_players(all_players, 3000, 60)
    variables, solution = run_solver(solver, all_players, max_flex)

    if solution == solver.OPTIMAL:
        roster = Roster()

        for i, player in enumerate(all_players):
            if variables[i].solution_value() == 1:
                roster.add_player(player)

        print "Optimal roster for: %s" % maxed_over
        print roster

    else:
      raise Exception('No solution error')


if __name__ == "__main__":
    subprocess.call(['python', 'scraper.py', argv[1]])
    for max_flex in ALL_LINEUPS.iterkeys():
        run(ALL_LINEUPS[max_flex], max_flex)