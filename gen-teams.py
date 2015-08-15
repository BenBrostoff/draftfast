import csv
from random import randint

all = []

TOP_POS = {}
ALL_POS = ['QB', 'RB', 'WR', 'TE', 'DST']
ALL_POS_TEAM = ['QB', 'RB1', 'RB2',
                'WR1', 'WR2', 'WR3',
                'TE', 'DST']

class Player:
    def __init__(self, pos, name, cost, proj=1):
        self.pos = pos
        self.name = name
        self.cost = cost
        self.proj = proj

    def player_report(self):
        print self.name + ' (' + self.cost + ')'

with open('dk-salaries-week-1.csv', 'rb') as dk:
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

for pos in ALL_POS:
    # eventually want to sort projected
    if pos == 'FLEX':
        filter_pos = [p for p in all if p.pos in ['QB', 'RB', 'WR']]
    else:
        filter_pos = [p for p in all if p.pos == pos]
    
    TOP_POS[pos] = sorted(filter_pos, key=lambda x: x.cost, reverse=True)[:20]

def choose_random(pos_list):
    return pos_list[(randint(0, len(pos_list) - 1))]

pos_dict = {
    'QB': TOP_POS['QB'],
    'RB1': TOP_POS['RB'],
    'RB2': TOP_POS['RB'],
    'WR1': TOP_POS['WR'],
    'WR2': TOP_POS['WR'],
    'WR3': TOP_POS['WR'],
    'FLEX': TOP_POS['QB'] + TOP_POS['WR'] + TOP_POS['RB'],
    'TE': TOP_POS['TE'],
    'DST': TOP_POS['DST']
}

class Team:
    def __init__(self):
        self._set_team_pos()
        self.team_cost = self._get_team_prop('proj')
        self.team_proj = self._get_team_prop('cost')

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

    def _set_team_pos(self):
        for k, v in pos_dict.iteritems():
            setattr(self, k, choose_random(v))

    def _get_team_prop(self, prop):
        cost = 0
        for pos in ALL_POS_TEAM:
            cost += int(getattr(getattr(self, pos), prop))

        return cost

teams = []
for x in xrange(0, 100000):
    team = Team()
    if not team.contains_dups():
        teams.append(team)

afford = [x for x in teams if x.team_cost <= 50000]
top_samp = sorted(afford, key=lambda x: x.team_proj, reverse=True)[0:5]

for team in top_samp:
    print '*****************'
    print team.team_report()
