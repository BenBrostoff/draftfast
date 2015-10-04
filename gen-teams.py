import time
import csv
import argparse
from sys import argv
from multiprocessing.dummy import Pool as ThreadPool 

from constants import * 
from lib.helpers import *
from orm import *

parser = argparse.ArgumentParser()

for opt in COMMAND_LINE:
    parser.add_argument(opt[0], help=opt[1], default=opt[2])

args = parser.parse_args()

all = []
TOP_POS = {}

with open('data/dk-salaries-week-1.csv', 'rb') as dk:
    rd = csv.reader(dk, delimiter=',')
    for idx, player in enumerate(rd):
        # skip header
        if idx > 0:
            pts = int(player[4].split('.')[0])
            all.append(Player(player[0], 
                              player[1], 
                              player[2],
                              pts))


# TODO - Yahoo / ESPN add projected; for now, use DK avg

# Set search config

search_settings = {
    'QB': {'d': args.qbd, 'p': args.qbp},
    'RB': {'d': args.rbd, 'p': args.rbp},
    'WR': {'d': args.wrd, 'p': args.wrp},
    'FLEX': {'d': args.flexd, 'p': args.flexp},
    'DST': {'d': args.dd, 'p': args.dp},
    'TE': {'d': args.dd, 'p': args.dp}
}

def get_avail_pos(all_avail, pos, proj_filter=0):
    cost_filter = search_settings[pos]['p']

    # Do not filter individually, filter by average
    if pos == 'RB' or pos == 'WR':
        cost_filter = 100000

    if pos == 'FLEX':
        return [p for p in all if p.pos in ['QB', 'RB', 'WR'] and \
                                 int(p.cost) < cost_filter and \
                                 int(p.proj) > proj_filter]

    return [p for p in all_avail if p.pos == pos and \
                                 int(p.cost) < cost_filter and \
                                 int(p.proj) > proj_filter]


def set_search_depth():
    '''sets positions to search on'''
    for pos in ALL_POS:
        filter_pos = get_avail_pos(all, pos)
        
        setting = search_settings[pos]['d']
        if setting < 4:
            raise Exception('Must search beyond top 3 at each position')

        TOP_POS[pos] = sorted(filter_pos, key=lambda x: x.proj, reverse=True)[:setting]

    # set multi-player positions and filter by average
    TOP_POS['MULTI_RB'] = get_combos(TOP_POS['RB'], 
                                     2, 
                                     search_settings['RB']['p'])
    TOP_POS['MULTI_WR'] = get_combos(TOP_POS['WR'], 
                                     3,
                                     search_settings['WR']['p'])

set_search_depth()

gather = cartesian((TOP_POS['QB'], 
                    TOP_POS['MULTI_RB'],
                    TOP_POS['MULTI_WR'],
                    TOP_POS['QB'] +  TOP_POS['WR'] +  TOP_POS['RB'],
                    TOP_POS['TE'],
                    TOP_POS['DST']))

hold = []
check = len(gather)

def split_list(lst, parts):
    sz = len(lst) / parts
    return [lst[i:i+sz] for i in range(0, len(lst), sz)]

def get_avail_teams(gather):
    check = len(gather)
    hold = []
    for idx, x in enumerate(gather):
        # 1 QB, 2RBs, 3 WRs, FLEX, TE, DST
        lineup = [x[0],
                  x[1].A0, x[1].A1,   
                  x[2].A0, x[2].A1, x[2].A2,
                  x[3], x[4], x[5]]

        team = Team(lineup)

        if team.team_cost <= 50000 and not team.contains_dups():
            hold.append(team)

    if len(hold) > 0:
        return sorted(hold, key=lambda x: x.team_proj, reverse=True)[0]


workers = int(args.wrk)
chunks = split_list(gather, workers)

pool = ThreadPool(workers) 
best = pool.map(get_avail_teams, chunks)

pool.close() 
pool.join() 

print sorted(best, key=lambda x: x.team_proj, reverse=True)[0].team_report()    
