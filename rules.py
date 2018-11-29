from abc import ABC, abstractmethod


class RuleSet(object):
    def __init__(self):
        self.rules = []

    def __iter__(self):
        return RulesIterator(self.rules)

    def __repr__(self):
        return '[' + ', '.join([repr(r) for r in self.rules]) + ']'

    def __str__(self):
        return '\n'.join(str(r) for r in self.rules)

    def __eq__(self, ruleset):
        if len(self.rules) != len(ruleset.rules):
            return False

        return set(self.rules) == set(ruleset)

    def _check_rule_conflicts(self):
        pass
        # raise RuleConflictException

    def _add_rule(self, rule):
        self._check_rule_conflicts()

        if rule not in self.rules:
            self.rules.append(rule)

    def add_group_rule(self, players, use):
        if len(players) != len(set(players)):
            raise RuleException('Duplicate player in group')

        if isinstance(use, (tuple, list)):
            if len(use) != 2:
                raise RuleException('Group rule use must be int or length 2')

            lo = use[0]
            hi = use[1]

            if hi == lo:
                if hi == len(players):
                    self.add_lock_rule(players)
                    return
                if hi == 0:
                    self.add_ban_rule(players)
                    return

            self._add_rule(PlayerGroupRule(players, lo, hi))
            return
        elif isinstance(use, int):
            if use == 0:
                self.add_ban_rule(players)
                return

            if use == len(players):
                self.add_lock_rule(players)
                return

            self._add_rule(PlayerGroupRule(players, use, use, exact=True))

    def add_ban_rule(self, players):
        self._add_rule(PlayerBanRule(players))

    def add_lock_rule(self, players):
        self._add_rule(PlayerLockRule(players))


class RuleConflictException(Exception):
    pass


class RulesIterator(object):
    def __init__(self, rules):
        self.rules = rules
        self.ndx = 0

    def __next__(self):
        if self.ndx >= len(self.rules):
            raise StopIteration

        r = self.rules[self.ndx]
        self.ndx += 1
        return r


class AbstractRule(ABC):
    @abstractmethod
    def __init__(self):
        super().__init__()

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __eq__(self):
        pass

    @abstractmethod
    def __hash__(self):
        pass


class RuleException(Exception):
    pass


class PlayerRule(AbstractRule):
    def __init__(self, players):
        if not len(players):
            raise RuleException('No players in group')

        if len(players) != len(set(players)):
            raise RuleException('Duplicate players in group')

        self.players = players

        super().__init__()

    def __repr__(self):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError

    def __eq__(self, rule):
        return set(self.players) == set(rule.players)

    def __hash__(self):
        return hash(''.join(sorted(self.players)))


class PlayerGroupRule(PlayerRule):
    def __init__(self, players, lo, hi, exact=False):
        super().__init__(players)
        self.lo = lo
        self.hi = hi
        self.exact = exact
        self._sanity_check()

    def __repr__(self):
        return '[{} of {}]'.format(self._bounds_str, self.players)

    def __str__(self):
        ls = ['Using {} of:'.format(self._bounds_str)] + \
             ['\t'+p for p in self.players]
        return '\n'.join(ls)

    def __eq__(self, rule):
        return super().__eq__(rule) and self.exact == rule.exact and \
               self.lo == rule.lo and self.hi == rule.hi

    def __hash__(self):
        return hash((super().__hash__(), self.exact, self.lo, self.hi))

    @property
    def _bounds_str(self):
        if self.exact:
            return '{0.lo}'.format(self)

        return '{0.lo} to {0.hi}'.format(self)

    def _sanity_check(self):
        if self.lo < 1:
            raise RuleException('Lower bound for group {!r} '.format(self) +
                                'cannot be less than 1'.format(self))

        if self.hi < self.lo:
            raise RuleException('Upper bound for group {!r} '.format(self) +
                                'cannot be less than lower bound.')

        if self.hi > len(self.players) or self.lo > len(self.players):
            raise RuleException('Bound for {!r} cannot be '.format(self) +
                                'greater than number of players in group')


class PlayerLockRule(PlayerRule):
    def __repr__(self):
        return '[LOCKED: {}]'.format(self.players)

    def __str__(self):
        ls = ['Locking:'] + ['\t'+p for p in self.players]
        return '\n'.join(ls)


class PlayerBanRule(PlayerRule):
    def __repr__(self):
        return '[BANNED: {}]'.format(self.players)

    def __str__(self):
        ls = ['Banning:'] + ['\t'+p for p in self.players]
        return '\n'.join(ls)


if __name__ == '__main__':
    rs1 = RuleSet()
    rs1.add_group_rule(['Eli Manning', 'Russell Wilson', 'Doug Martin'], (1, 3))
    rs1.add_group_rule(['Will Fuller'], 1)
    rs1.add_group_rule(['Spencer Ware', 'Amari Cooper'], 1)
    rs1.add_group_rule(['Packers'], 0)

    print(repr(rs1))
    print(rs1)
    print()

    rs2 = RuleSet()
    rs2.add_group_rule(['Spencer Ware', 'Amari Cooper'], 1)
    rs2.add_ban_rule(['Packers'])
    rs2.add_group_rule(['Eli Manning', 'Russell Wilson', 'Doug Martin'], (1, 3))
    rs2.add_lock_rule(['Will Fuller'])
    rs2 = RuleSet()
    rs2.add_group_rule(['Eli Manning', 'Russell Wilson', 'Doug Martin'], (1, 3))
    rs2.add_lock_rule(['Will Fuller'])
    rs2.add_group_rule(['Spencer Ware', 'Amari Cooper'], 1)
    rs2.add_ban_rule(['Packers'])
    rs2.add_group_rule(['Eli Manning', 'Russell Wilson', 'Doug Martin'], (1, 3))
    rs2.add_group_rule(['Will Fuller'], 1)
    rs2.add_group_rule(['Spencer Ware', 'Amari Cooper'], 1)
    rs2.add_group_rule(['Packers'], 0)
    rs2.add_group_rule(['Eli Manning', 'Doug Martin', 'Russell Wilson'], (1, 3))

    print(repr(rs2))
    print(rs2)
    print()

    if rs1 == rs2:
        print('PASS')
    else:
        print('FAIL')
