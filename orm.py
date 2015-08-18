from constants import ALL_POS_TEAM

class Player:
    def __init__(self, pos, name, cost, proj):
        self.pos = pos
        self.name = name
        self.cost = int(cost)
        self.proj = proj

    def player_report(self):
        print self.pos + ' '+ self.name + \
        ' (' + str(self.cost) + ')' + ' (' + str(self.proj) + ')'

    def __repr__(self):
        return "[{0: <2}] {1: <20}(${2}, {3})".format(self.pos, \
                                    self.name, \
                                    self.cost, \
                                    self.proj)

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