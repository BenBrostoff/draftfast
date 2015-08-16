import threading
import time
from sys import argv
import csv
from lib.helpers import *

all = []

TOP_POS = {}
ALL_POS = ['QB', 'RB', 'WR', 'TE', 'DST']
ALL_POS_TEAM = ['QB', 'RB1', 'RB2',
                'WR1', 'WR2', 'WR3', 'FLEX',
                'TE', 'DST']

class Player:
    def __init__(self, pos, name, cost, proj):
        self.pos = pos
        self.name = name
        self.cost = cost
        self.proj = proj

    def player_report(self):
        print self.pos + ' '+ self.name + \
        ' (' + self.cost + ')' + ' (' + str(self.proj) + ')'

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
qbs = int(argv[1])
flex = int(argv[2])
te = int(argv[3])
dst = int(argv[4])

search_settings = {
    'QB': int(argv[1]),
    'RB': int(argv[2]),
    'WR': int(argv[3]),
    'FLEX': int(argv[4]),
    'DST': int(argv[5]),
    'TE': int(argv[6])
}

def get_avail_pos(all_avail, cost_filter=0, proj_filter=0):
    return [p for p in all_avail if p.pos == pos and \
                                 int(p.cost) > cost_filter and \
                                 int(p.proj) > proj_filter]

for pos in ALL_POS:
    # eventually want to sort projected
    print pos
    if pos == 'FLEX':
        filter_pos = [p for p in all if p.pos in ['QB', 'RB', 'WR'] and int(p.cost) < 7000]
    elif pos == 'QB':
        filter_pos = [p for p in all if p.pos == pos and int(p.cost) and int(p.cost) < 7000]
    elif pos == 'TE':
        filter_pos = [p for p in all if p.pos == pos and int(p.cost) < 7000]
    elif pos == 'DST':
        filter_pos = [p for p in all if p.pos == pos and int(p.cost) > 2000]
    else:
        filter_pos = [p for p in all if p.pos == pos]
    
    setting = search_settings[pos]
    if setting < 4:
        raise Exception('Must search beyond top 3 at each position')

    TOP_POS[pos] = sorted(filter_pos, key=lambda x: x.proj, reverse=True)[:setting]

class Team:
    def __init__(self, give):
        self._set_team_pos(give)
        self.team_cost = self._get_team_prop('cost')
        self.team_proj = self._get_team_prop('proj')

    def team_report(self):
        for pos in ALL_POS_TEAM:
            getattr(self, pos).player_report()

        print 'Total Cost: ' + str(self.team_cost)
        print 'Total Projected: ' + str(self.team_proj)

    def contains_dups(self):
        players = []
        for pos in ALL_POS_TEAM:
            name = getattr(self, pos).name
            players.append(name)

        return len(players) != len(set(players))  

    def _set_team_pos(self, give):
        for idx, val in enumerate(give):
            setattr(self, ALL_POS_TEAM[idx], val)

    def _get_team_prop(self, prop):
        val = 0
        for pos in ALL_POS_TEAM:
            val += int(getattr(getattr(self, pos), prop))

        return val


rbs = get_combos(TOP_POS['RB'], 2, 6500)
wrs = get_combos(TOP_POS['WR'], 3, 6500)

print rbs[0]    
print wrs[0]
print len(rbs)
print len(wrs)
time.sleep(3)

gather = cartesian((TOP_POS['QB'], 
                    rbs,
                    wrs,
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
        print str(idx) + ' of ' + str(check) + '...'

        # 1 QB, 2RBs, 3 WRs, FLEX, TE, DST
        lineup = [x[0],
                  x[1].A0, x[1].A1,   
                  x[2].A0, x[2].A1, x[2].A2,
                  x[3], x[4], x[5]]

        team = Team(lineup)

        if team.team_cost <= 50000 and not team.contains_dups():
            hold.append(team)
    if len(hold) > 0:
        print sorted(hold, key=lambda x: x.team_proj, reverse=True)[0].team_report()
        print sorted(hold, key=lambda x: x.team_proj, reverse=True)[1].team_report()

class myThread (threading.Thread):
    def __init__(self, name, chunk):
        threading.Thread.__init__(self)
        self.name = name
        self.chunk = chunk
    def run(self):
        print 'Running ' + self.name
        get_avail_teams(self.chunk)

get_avail_teams(gather)
    
