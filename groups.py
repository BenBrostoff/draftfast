class PlayerGroupException(Exception):
    pass


class PlayerGroup(object):
    def __init__(self, players, play_str):
        if not len(players):
            raise PlayerGroupException('No players found in group')
        if not len(play_str):
            raise PlayerGroupException('Play string is empty')

        self.players = players
        self.min = None
        self.max = None
        self.exact = None

        self._split_play_str(play_str)

    def _split_play_str(self, s):
        s = s.split('-')
        lo = int(s[0])

        if lo < 0:
            raise PlayerGroupException('Lower bound cannot be less than zero')

        if len(s) == 2:
            hi = int(s[1])

            # hi = lo = 0 is ok
            if(lo == 0 and hi != 0):
                raise PlayerGroupException('Lower bound cannot be zero when ' +
                                           'upper bound is greater than zero')

            if hi < lo:
                raise PlayerGroupException('Upper bound cannot be less than ' +
                                           'lower bound')

            if lo == hi:
                self.exact = lo
            else:
                self.min = lo
                self.max = hi
        elif len(s) == 1:
            self.exact = lo
        else:
            raise PlayerGroupException('Group must have one or two bounds')

        if self.exact and len(self.players) <= self.exact:
            raise PlayerGroupException('Bound cannot be greater than ' +
                                       'number of players in group')

        if self.max and len(self.players) <= self.max:
            raise PlayerGroupException('Bound cannot be greater than ' +
                                       'number of players in group')

        if self.min and len(self.players) <= self.min:
            raise PlayerGroupException('Bound cannot be greater than ' +
                                       'number of players in group')

    def __repr__(self):
        s = 'Using '
        if self.exact:
            s += str(self.exact)
        else:
            s += '{0.min} to {0.max}'.format(self)
        s += '\n'

        for p in self.players:
            s += '\t'+p +'\n'

        return s


class PlayerGroups(object):
    def __init__(self, groupfile):
        self.groups = []
        self.parse_groups(groupfile)

    def __repr__(self):
        s = ''
        for g in self.groups:
            s += str(g)
        return s

    def parse_groups(self, groupfile):
        with open(groupfile) as f:
            for line in f.read().splitlines():
                if not line:
                    continue

                if line == 'OF':
                    players = []
                elif line.startswith('PLAY'):
                    self.groups.append(PlayerGroup(players, line.split()[1]))
                else:
                    players.append(line)


if __name__ == '__main__':
    g = PlayerGroups('test/data/groups.csv')
    print(g)
