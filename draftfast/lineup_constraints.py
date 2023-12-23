from abc import ABC, abstractmethod


def _iterableify(x):
    if isinstance(x, (str)):
        return [x]
    return x


class LineupConstraints(object):
    def __init__(
        self,
        locked: list = [],
        position_locked: list = [],
        banned: list = [],
        position_banned: list = [],
        groups: list = [],
    ):
        self._constraints = []
        self._banned = set()
        self._locked = set()
        self._position_locked = set()
        self._position_banned = set()

        for name in banned:
            self.ban(name)

        for solver_id in position_banned:
            self.position_ban(solver_id)

        for solver_id in position_locked:
            self.position_lock(solver_id)

        for name in locked:
            self.lock(name)

        for players, bounds in groups:
            self.add_group_constraint(players, bounds)

    def exist(self):
        return len(self)

    def __iter__(self):
        return ConstraintIterator(self._constraints)

    def __len__(self):
        return (
            len(self._constraints)
            + len(self._locked)
            + len(self._banned)
            + len(self._position_locked)
            + len(self._position_banned)
        )

    def __repr__(self):
        constraints = ", ".join([repr(c) for c in self._constraints])
        lcs = "LineupConstraintSet: {}".format(constraints)
        b1 = "<Banned: {!r}>".format(self._banned)
        bp1 = "<PositionBanned: {!r}>".format(self._position_banned)
        lp1 = "<Locked: {!r}>".format(self._locked)
        l1 = "<PositionLocked: {!r}>".format(self._position_locked)
        return "<{}, {}, {}, {}, {}>".format(lcs, b1, bp1, l1, lp1)

    def __str__(self):
        lines = [str(c) for c in self._constraints]
        if len(self._banned):
            lines.append("Banned: " + ", ".join(p for p in self._banned))
        if len(self._locked):
            lines.append("Locked: " + ", ".join(p for p in self._locked))
        if len(lines):
            return "\n".join(lines)
        else:
            return "None"

    def __eq__(self, constraintset):
        if len(self._constraints) != len(constraintset._constraints):
            return False

        if set(self._constraints) != set(constraintset._constraints):
            return False

        if self._locked != constraintset._locked:
            return False

        if self._banned != constraintset._banned:
            return False

        if self._position_locked != constraintset._position_locked:
            return False

        if self._position_banned != constraintset._position_banned:
            return False

        return True

    def __contains__(self, player):
        if player in self._locked:
            return True

        if player in self._banned:
            return True

        for c in self._constraints:
            if isinstance(c, PlayerGroupConstraint):
                if player in c.players:
                    return True

        return False

    def _check_conflicts(self, constraint):
        if isinstance(constraint, PlayerGroupConstraint):
            for p in constraint.players:
                if p in self._locked or p in self._banned:
                    raise ConstraintConflictException(
                        "Ban/lock constraint for {} already exists".format(p)
                    )

    def _add(self, constraint):
        self._check_conflicts(constraint)

        if constraint not in self._constraints:
            self._constraints.append(constraint)
        else:
            raise ConstraintConflictException("Duplicate constraint")

    def is_banned(self, player: str) -> bool:
        return player in self._banned

    def is_locked(self, player: str) -> bool:
        return player in self._locked

    def is_position_locked(self, solver_id: str) -> bool:
        return solver_id in self._position_locked

    def is_position_banned(self, solver_id: str) -> bool:
        return solver_id in self._position_banned

    def has_group_constraints(self) -> bool:
        return len(self._constraints) != 0

    def add_group_constraint(self, players, bound):
        self._add(PlayerGroupConstraint(players, bound))

    def ban(self, players):
        _players = _iterableify(players)

        if len(_players) == 0:
            raise ConstraintException("Empty ban group")

        for p in _players:
            if p in self:
                raise ConstraintConflictException(
                    "{} exists in another constraint".format(p)
                )
        self._banned.update(_players)

    def lock(self, players):
        _players = _iterableify(players)

        if len(_players) == 0:
            raise ConstraintException("Empty lock group")

        for p in _players:
            if p in self:
                raise ConstraintConflictException(
                    "{} exists in another constraint".format(p)
                )
        self._locked.update(_players)

    def position_lock(self, solver_ids):
        _solver_ids = _iterableify(solver_ids)

        if len(_solver_ids) == 0:
            raise ConstraintException("Empty position lock group")

        for p in _solver_ids:
            if p in self:
                raise ConstraintConflictException(
                    "{} exists in another constraint".format(p)
                )
        self._position_locked.update(_solver_ids)

    def position_ban(self, solver_ids):
        _solver_ids = _iterableify(solver_ids)

        if len(_solver_ids) == 0:
            raise ConstraintException("Empty position lock group")

        for p in _solver_ids:
            if p in self:
                raise ConstraintConflictException(
                    "{} exists in another constraint".format(p)
                )
        self._position_banned.update(_solver_ids)


class ConstraintConflictException(Exception):
    pass


class ConstraintIterator(object):
    def __init__(self, constraints):
        self._constraints = constraints
        self.ndx = 0

    def __next__(self):
        if self.ndx >= len(self._constraints):
            raise StopIteration

        r = self._constraints[self.ndx]
        self.ndx += 1
        return r


class AbstractConstraint(ABC):
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
    def __eq__(self, constraint):
        pass

    @abstractmethod
    def __hash__(self):
        pass

    @abstractmethod
    def __contains__(self, player):
        pass


class ConstraintException(Exception):
    pass


class PlayerConstraint(AbstractConstraint):
    def __init__(self, players):
        if not len(players):
            raise ConstraintException("No players in group")

        if len(players) != len(set(players)):
            raise ConstraintException("Duplicate players in group")

        self.players = players

        super().__init__()

    def __eq__(self, rule):
        return set(self.players) == set(rule.players)

    def __hash__(self):
        return hash("".join(sorted(self.players)))

    def __contains__(self, player):
        return player in self.players


class PlayerGroupConstraint(PlayerConstraint):
    def __init__(self, players, bound):
        super().__init__(players)
        self.exact = None
        self.lb = None
        self.ub = None

        if isinstance(bound, (list, tuple)) and len(bound) == 2:
            self.lb = bound[0]
            self.ub = bound[1]
            self._ub_lb_bounds_sanity_check()
        elif isinstance(bound, int):
            self.exact = bound
            self._exact_bounds_sanity_check()
        else:
            raise ConstraintException("Bound must be length 2 or int")

    def __repr__(self):
        return "<PlayerGroupConstraint: {} of {}>".format(
            self._bounds_str, self.players
        )

    def __str__(self):
        return "Using {} of: {}".format(
            self._bounds_str, ", ".join(p for p in self.players)
        )

    def __eq__(self, constraint):
        return (
            super().__eq__(constraint)
            and self.exact == constraint.exact
            and self.lb == constraint.lb
            and self.ub == constraint.ub
        )

    def __hash__(self):
        return hash((super().__hash__(), self.exact, self.lb, self.ub))

    @property
    def _bounds_str(self):
        if self.exact:
            return "{0.exact}".format(self)

        return "{0.lb} to {0.ub}".format(self)

    def _exact_bounds_sanity_check(self):
        if self.exact <= 0:
            raise ConstraintException(
                "Exact bound may not less than or equal to zero"
            )
        if self.exact >= len(self.players):
            raise ConstraintException(
                "Exact bound may not be greater than or equal to number "
                "of players in group"
            )

    def _ub_lb_bounds_sanity_check(self):
        if self.lb < 1:
            raise ConstraintException(
                "Lower bound for {!r} cannot be less than 1".format(self)
            )
        if self.ub == self.lb:
            raise ConstraintException(
                "Lower bound for {!r} cannot equal upper bound".format(self)
            )
        if self.ub < self.lb:
            raise ConstraintException(
                "Upper bound for {!r} cannot be less than lower bound.".format(
                    self
                )
            )
        if self.ub > len(self.players) or self.lb > len(self.players):
            raise ConstraintException(
                "Bound for {!r} cannot be greater than number of players "
                "group".format(self)
            )
