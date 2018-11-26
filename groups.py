import re


class PlayerGroupException(Exception):
    pass


class PlayerGroup(object):
    def __init__(self, players, play_str):
        if not len(players):
            raise PlayerGroupException('No players found in group')
        if not len(play_str):
            raise PlayerGroupException('Play string is empty')

        if not re.match(r'^(\d+-\d+)|(\d+)$', play_str):
            raise PlayerGroupException('Malformed play string: {}'
                                       .format(play_str))

        self.players = players
        self.force_banned = False
        self.force_locked = False

        self._split_play_str(play_str)

    def __repr__(self):
        s = '[[{} of {}]]'.format(self._bounds_str(), self.players)

        if self.force_banned:
            return s + ' (BANNED)'
        if self.force_locked:
            return s + ' (LOCKED)'

        return s

    def __str__(self):
        ls = []
        ls.append('Using {} of:'.format(self._bounds_str()))
        for p in self.players:
            ls.append('\t' + p)

        if self.force_banned:
            ls.append('All pjayers BANNED')

        if self.force_locked:
            ls.append('All players LOCKED')

        return '\n'.join(ls)

    def _is_exact(self):
        return hasattr(self, 'exact')

    def _is_min_max(self):
        return hasattr(self, 'min')

    def _split_play_str(self, s):
        s = s.split('-')
        lo = int(s[0])

        if lo < 0:
            raise PlayerGroupException('Lower bound for group {} cannot be ' +
                                       'less than zero'
                                       .format(self.__repr__()))

        if len(s) == 2:
            hi = int(s[1])

            # hi = lo = 0 is ok
            if(lo == 0 and hi != 0):
                raise PlayerGroupException('Lower bound for group {} cannot ' +
                                           'be 0 when upper bound is >0'
                                           .format(self.__repr__()))

            if hi < lo:
                raise PlayerGroupException('Upper bound for group ' +
                                           self.__repr__() +
                                           ' cannot be less than lower bound.')

            if lo == hi:
                self.exact = lo
            else:
                self.min = lo
                self.max = hi
        elif len(s) == 1:
            self.exact = lo
        else:
            raise PlayerGroupException('Group {} must have one or two bounds'
                                       .format(self.__repr__()))

        if (self._is_exact() and self.exact > len(self.players)) or \
           (self._is_min_max() and (self.max > len(self.players) or
                                    self.min > len(self.players))):
            raise PlayerGroupException('Bound for ' +
                                       '{}'.format(self.__repr__()) +
                                       ' cannot be greater than number of' +
                                       ' players in group')

        if self._is_exact() and self.exact == 0:
            self.force_banned = True
        elif self._is_exact() and self.exact == len(self.players):
            self.force_locked = True

    def _bounds_str(self):
        if self._is_exact():
            return str(self.exact)

        if self._is_min_max():
            return '{0.min} to {0.max}'.format(self)

        return None


class PlayerGroups(object):
    def __init__(self, groupfile):
        self.groups = []
        self.parse_groups(groupfile)

    def __repr__(self):
        return '\n'.join(self.groups)

    def __str__(self):
        ls = []
        for g in self.groups:
            ls.append(str(g))

        return '\n'.join(ls)

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
