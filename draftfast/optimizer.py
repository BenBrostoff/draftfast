from ortools.linear_solver import pywraplp
from draftfast.settings import OptimizerSettings
from draftfast.dke_exceptions import InvalidBoundsException


class Optimizer(object):
    def __init__(
        self,
        players,
        rule_set,
        settings,
        constraints,
    ):
        settings = settings or OptimizerSettings()
        self.solver = pywraplp.Solver(
            'FD',
            pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING
        )
        self.players = players
        self.enumerated_players = list(enumerate(players))
        self.existing_rosters = settings.existing_rosters or []
        self.salary_min = rule_set.salary_min
        self.salary_max = rule_set.salary_max
        self.roster_size = rule_set.roster_size
        self.position_limits = rule_set.position_limits
        self.general_position_limits = rule_set.general_position_limits
        self.settings = settings
        self.constraints = constraints

        self.player_to_idx_map = {}
        self.variables = []
        for idx, player in self.enumerated_players:
            self.variables.append(
                self.solver.IntVar(0, 1, player.solver_id)
            )

            self.player_to_idx_map[player.solver_id] = idx

        self.objective = self.solver.Objective()
        self.objective.SetMaximization()

    def solve(self):
        self._set_player_constraints()
        self._optimize_on_projected_points()
        self._set_salary_range()
        self._set_roster_size()
        self._set_positions()
        self._set_general_positions()
        self._set_stack()
        self._set_combo()
        self._set_no_duplicate_lineups()
        solution = self.solver.Solve()
        return solution == self.solver.OPTIMAL

    def _set_player_constraints(self):
        multi_constraints = dict()

        for i, p in self.enumerated_players:
            lb = 1 if self.constraints.is_locked(p.name) else 0
            ub = 0 if self.constraints.is_banned(p.name) else 1

            if lb > ub:
                raise InvalidBoundsException

            if p.multi_position:
                if p.name not in multi_constraints.keys():
                    multi_constraints[p.name] = self.solver.Constraint(lb,ub)
                constraint = multi_constraints[p.name]
            else:
                constraint = self.solver.Constraint(lb, ub)

            constraint.SetCoefficient(self.variables[i], 1)

    def _optimize_on_projected_points(self):
        for i, player in self.enumerated_players:
            self.objective.SetCoefficient(
                self.variables[i],
                player.proj,
            )

    def _set_salary_range(self):
        salary_cap = self.solver.Constraint(
            self.salary_min,
            self.salary_max,
        )
        for i, player in self.enumerated_players:
            salary_cap.SetCoefficient(
                self.variables[i],
                player.cost
            )

    def _set_roster_size(self):
        size_cap = self.solver.Constraint(
            self.roster_size,
            self.roster_size,
        )

        for variable in self.variables:
            size_cap.SetCoefficient(variable, 1)


    def _set_stack(self):
        if self.settings:
            stack = self.settings.stack_team
            stack_count = self.settings.stack_count

            if stack and stack_count:
                position_cap = self.solver.Constraint(
                    stack_count,
                    stack_count,
                )

                for i, player in self.enumerated_players:
                    if stack == player.team:
                        position_cap.SetCoefficient(
                            self.variables[i],
                            1
                        )

    def _set_combo(self):
        if self.settings:
            combo = self.settings.force_combo
            combo_allow_te = self.settings.combo_allow_te

            combo_skill_type = ['WR']
            if combo_allow_te:
                combo_skill_type.append('TE')

            if combo:
                teams = set([p.team for p in self.players])
                enumerated_players = self.enumerated_players

                for team in teams:
                    wrs_on_team = [
                        self.variables[i] for i, p in enumerated_players
                        if p.team == team and p.pos in combo_skill_type
                    ]
                    qbs_on_team = [
                        self.variables[i] for i, p in enumerated_players
                        if p.team == team and p.pos == 'QB'
                    ]
                    self.solver.Add(
                        self.solver.Sum(wrs_on_team) >=
                        self.solver.Sum(qbs_on_team)
                    )

    def _set_positions(self):
        for position, min_limit, max_limit in self.position_limits:
            position_cap = self.solver.Constraint(
                min_limit,
                max_limit
            )

            for i, player in self.enumerated_players:
                if position == player.pos:
                    position_cap.SetCoefficient(self.variables[i], 1)

    def _set_general_positions(self):
        for general_position, min_limit, max_limit in \
                self.general_position_limits:
            position_cap = self.solver.Constraint(min_limit, max_limit)

            for i, player in self.enumerated_players:
                if general_position == player.nba_general_position:
                    position_cap.SetCoefficient(
                        self.variables[i],
                        1
                    )

    def _set_no_duplicate_lineups(self):
        for roster in self.existing_rosters:
            max_repeats = self.roster_size - 1
            if self.settings.uniques:
                max_repeats = max(
                    self.roster_size - self.settings.uniques,
                    1
                )
            repeated_players = self.solver.Constraint(
                0,
                max_repeats
            )
            for player in roster.sorted_players():
                i = self.player_to_idx_map.get(player.solver_id)
                if i is not None:
                    repeated_players.SetCoefficient(self.variables[i], 1)
