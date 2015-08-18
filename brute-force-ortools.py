# A huge thanks to swanson
# this solution is almost wholly based off
# https://github.com/swanson/degenerate

import time
import csv
from ortools.linear_solver import pywraplp
from orm import *
from constants import *

class Roster:
  POSITION_ORDER = {
    "QB": 0,
    "RB": 1,
    "WR": 2,
    "TE": 3,
    "DST": 4
  }

  def __init__(self):
    self.players = []

  def add_player(self, player):
    self.players.append(player)

  def spent(self):
    return sum(map(lambda x: x.cost, self.players))

  def projected(self):
    return sum(map(lambda x: x.proj, self.players))

  def position_order(self, player):
    return self.POSITION_ORDER[player.pos]

  def sorted_players(self):
    return sorted(self.players, key=self.position_order)

  def __repr__(self):
    s = '\n'.join(str(x) for x in self.sorted_players())
    s += "\n\nProjected Score: %s" % self.projected()
    s += "\tCost: $%s" % self.spent()
    return s

SALARY_CAP = 50000

ROSTER_SIZE = 9

def run(max_flex):
  solver = pywraplp.Solver('FD', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

  all_players = []
  with open('data/dk-salaries-week-1.csv', 'rb') as csvfile:
    csvdata = csv.reader(csvfile, skipinitialspace=True)

    for idx, row in enumerate(csvdata):
      if idx > 0:
        pts = int(row[4].split('.')[0])
        all_players.append(Player(row[0], row[1], row[2], pts))

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

  solution = solver.Solve()

  if solution == solver.OPTIMAL:
    roster = Roster()

    for i, player in enumerate(all_players):
      if variables[i].solution_value() == 1:
        roster.add_player(player)

    print "Optimal roster for: $%s\n" % SALARY_CAP
    print roster

  else:
    print "No solution :("


if __name__ == "__main__":
  for max_flex in ALL_LINEUPS:
    run(max_flex)