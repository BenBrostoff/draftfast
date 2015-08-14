import csv
from random import randint

all = []

with open('dk-salaries-week-1.csv', 'rb') as dk:
    rd = csv.reader(dk, delimiter=',')
    for player in rd:
        all.append(player)

def pos_gather(pos, top=20):
    select = [x for x in all if x[0] == pos]
    select = sorted(select, key=lambda x: int(x[2]), reverse=True)
    return select[:top]

TEAM_REQS = {
    'QB': 1,
    'RB': 2,
    'WR': 3,
    'TE': 1,
    'DST': 1  
}

class Team:    
    def __init__(self):
        team = {}
        for pos, number in TEAM_REQS.iteritems():
            team[pos] = self.choose_random(pos, number)

        self.team = team
        self.cost = 0
        for pos, info in self.team.iteritems():
            if type(info[0]) is not list:
                self.cost += int(info[2])
            else:
                for x in info: 
                    self.cost += int(x[2])
            
    def choose_random(self, position, needed=1):
        mult, avail = [], pos_gather(position)
        if needed == 1:
            return avail[randint(0, len(avail) - 1)]
        else:
            for x in xrange(0, needed):
                mult.append(avail[randint(0, len(avail) - 1)])
            return mult

    def team_report(self):
        for pos, info in self.team.iteritems():
            print pos + ':' 
            if type(info[0]) is not list:
                print info[1]
            else:
                for x in info:
                    print x[1]  
        print "Team Cost" + ": " + str(self.cost)

random_samp = []
for x in xrange(0, 100):
    random_samp.append(Team())

random_samp = sorted(random_samp, key=lambda x: abs(x.cost - 50000))
random_samp = [x for x in random_samp if x.cost <= 50000]

for x in random_samp:
    x.team_report()  
