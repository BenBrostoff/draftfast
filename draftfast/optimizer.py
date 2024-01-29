from typing import List
from ortools.linear_solver import pywraplp
from draftfast.settings import OptimizerSettings
from draftfast.dke_exceptions import (
    InvalidBoundsException,
    PlayerBanAndLockException,
)
from draftfast.orm import Player
from draftfast.rules import RuleSet, DK_NHL_RULE_SET
from draftfast.lineup_constraints import LineupConstraints


class Optimizer(object):
    def __init__(
        self,
        players: List[Player],
        rule_set: RuleSet,
        settings: OptimizerSettings,
        lineup_constraints: LineupConstraints,
        exposure_dict: dict,
    ):
        self.rule_set = rule_set
        self.solver = pywraplp.Solver(
            "FD", pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING
        )
        self.players = players
        self.enumerated_players = list(enumerate(players))
        self.existing_rosters = settings.existing_rosters or []
        self.salary_min = rule_set.salary_min
        self.salary_max = rule_set.salary_max
        self.roster_size = rule_set.roster_size
        self.position_limits = rule_set.position_limits
        self.offensive_positions = rule_set.offensive_positions
        self.defensive_positions = rule_set.defensive_positions
        self.general_position_limits = rule_set.general_position_limits
        self.max_players_per_team = rule_set.max_players_per_team
        self.showdown = rule_set.game_type == "showdown"
        self.settings = settings
        self.lineup_constraints = lineup_constraints
        self.banned_for_exposure = exposure_dict.get("banned", [])
        self.locked_for_exposure = exposure_dict.get("locked", [])
        self.custom_rules = (rule_set.custom_rules or []) + (settings.custom_rules or [])
        self.min_teams = rule_set.min_teams or settings.min_teams
        self.min_matchups = rule_set.min_matchups or settings.min_matchups
        self.position_per_team_rules = rule_set.position_per_team_rules

        self.player_to_idx_map = {}
        self.name_to_idx_map = {}
        self.variables = []
        self.name_to_idx_map = dict()
        self.player_to_idx_map = dict()

        for idx, player in self.enumerated_players:
            self.variables.append(self.solver.IntVar(0, 1, player.solver_id))

            self._add_player_to_idx_maps(player, idx)

            if self._is_locked(player):
                player.lock = True
            if self._is_banned(player):
                player.ban = True
            if self._is_position_locked(player):
                player.position_lock = True
            if self._is_position_banned(player):
                player.position_ban = True

            # TODO: this can only happen because of exposure, but it could be
            # handled better
            if player.lock and player.ban:
                raise PlayerBanAndLockException(player.name)

        self.teams = set([p.team for p in self.players])
        if self.min_matchups:
            self.matchups = set([p.matchup for p in self.players])
        self.objective = self.solver.Objective()
        self.objective.SetMaximization()

    def _add_player_to_idx_maps(self, p: Player, idx: int):
        self.player_to_idx_map[p.solver_id] = idx

        if p.name not in self.name_to_idx_map.keys():
            self.name_to_idx_map[p.name] = set()
        self.name_to_idx_map[p.name].update([idx])

    def _is_locked(self, p: Player) -> bool:
        return (
            self.lineup_constraints.is_locked(p.name)
            or p.name in self.locked_for_exposure
            or p.lock
        )

    def _is_banned(self, p: Player) -> bool:
        return (
            self.lineup_constraints.is_banned(p.name)
            or p.name in self.banned_for_exposure
            or p.ban
        )

    def _is_position_locked(self, p: Player) -> bool:
        return self.lineup_constraints.is_position_locked(p.solver_id)

    def _is_position_banned(self, p: Player) -> bool:
        return self.lineup_constraints.is_position_banned(p.solver_id)

    def solve(self) -> bool:
        self._set_player_constraints()
        self._set_player_group_constraints()
        self._optimize_on_projected_points()
        self._set_salary_range()
        self._set_roster_size()
        self._set_positions()
        self._set_general_positions()
        self._set_stack()
        self._set_combo()
        self._set_no_duplicate_lineups()
        self._set_min_teams()
        self._set_min_matchups()
        self._set_custom_rules()
        self._set_position_team_constraints()

        if (
            self.offensive_positions
            and self.defensive_positions
            and self.settings.no_offense_against_defense
            or self.showdown
            and self.settings.no_defense_against_captain
        ):
            self._set_no_opp_defense()

        solution = self.solver.Solve()

        return solution == self.solver.OPTIMAL

    def _set_player_constraints(self):
        multi_constraints = dict()

        for i, p in self.enumerated_players:
            lb = 1 if (p.lock or p.position_lock) else 0
            ub = 0 if (p.ban or p.position_ban) else 1

            if lb > ub:
                raise InvalidBoundsException(
                    "Invalid bounds for {}".format(p.name)
                )

            if (p.multi_position or self.showdown) and not (
                p.position_lock or p.position_ban
            ):
                if p.name not in multi_constraints.keys():
                    multi_constraints[p.name] = self.solver.Constraint(lb, ub)
                constraint = multi_constraints[p.name]
            elif (p.multi_position or self.showdown) and p.position_lock:
                if p.name not in multi_constraints.keys():
                    multi_constraints[p.name] = self.solver.Constraint(0, ub)
                multi_constraints[p.name].SetCoefficient(self.variables[i], 1)

                constraint = self.solver.Constraint(lb, ub)
            else:
                constraint = self.solver.Constraint(lb, ub)

            constraint.SetCoefficient(self.variables[i], 1)

    def _set_player_group_constraints(self):
        for group_constraint in self.lineup_constraints:
            if group_constraint.exact:
                lb = ub = group_constraint.exact
            else:
                lb = group_constraint.lb
                ub = group_constraint.ub

            constraint = self.solver.Constraint(lb, ub)
            for name in group_constraint.players:
                for idx in self.name_to_idx_map[name]:
                    constraint.SetCoefficient(self.variables[idx], 1)

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
            salary_cap.SetCoefficient(self.variables[i], player.cost)

    def _set_roster_size(self):
        size_cap = self.solver.Constraint(
            self.roster_size,
            self.roster_size,
        )

        for variable in self.variables:
            size_cap.SetCoefficient(variable, 1)

    def _set_stack(self):
        if self.settings:
            stacks = self.settings.stacks

            if stacks:
                for stack in stacks:
                    stack_team = stack.team
                    stack_count = stack.count
                    stack_lock_pos = stack.stack_lock_pos
                    stack_lock_eligible_pos = stack.stack_eligible_pos

                    stack_cap = self.solver.Constraint(
                        stack_count,
                        stack_count,
                    )

                    for i, player in self.enumerated_players:
                        if stack_team == player.team:
                            stack_cap.SetCoefficient(self.variables[i], 1)

                    self._set_stacking_type(
                        stack_lock_pos,
                        stack_lock_eligible_pos,
                        stack_team,
                        stack.count,
                    )

    def _set_stacking_type(
        self,
        stack_lock_pos,
        stack_eligible_pos,
        team,
        count,
    ):
        if self.settings:
            if stack_lock_pos and stack_eligible_pos:
                enumerated_players = self.enumerated_players

                skillplayers_on_team = [
                    self.variables[i]
                    for i, p in enumerated_players
                    if p.team == team and p.pos in stack_eligible_pos
                ]
                locked_on_team = [
                    self.variables[i]
                    for i, p in enumerated_players
                    if p.team == team and p.pos == stack_lock_pos
                ]
                self.solver.Add(
                    self.solver.Sum(skillplayers_on_team)
                    >= self.solver.Sum(locked_on_team)
                )
                self.solver.Add(
                    (self.solver.Sum(skillplayers_on_team)) >= count - 1
                )

    def _set_combo(self):
        if self.settings:
            combo = self.settings.force_combo
            combo_allow_te = self.settings.combo_allow_te

            combo_skill_type = ["WR"]
            if combo_allow_te:
                combo_skill_type.append("TE")

            if combo:
                teams = set([p.team for p in self.players])
                enumerated_players = self.enumerated_players

                for team in teams:
                    skillplayers_on_team = [
                        self.variables[i]
                        for i, p in enumerated_players
                        if p.team == team and p.pos in combo_skill_type
                    ]
                    qbs_on_team = [
                        self.variables[i]
                        for i, p in enumerated_players
                        if p.team == team and p.pos == "QB"
                    ]
                    self.solver.Add(
                        self.solver.Sum(skillplayers_on_team)
                        >= self.solver.Sum(qbs_on_team)
                    )

    def _set_no_opp_defense(self):
        offensive_pos = self.offensive_positions
        defensive_pos = self.defensive_positions

        enumerated_players = self.enumerated_players

        for team in self.teams:
            offensive_against = [
                self.variables[i]
                for i, p in enumerated_players
                if p.pos in offensive_pos
                and p.is_opposing_team_in_match_up(team)
            ]

            # TODO this is gross for showdown
            defensive = [
                self.variables[i]
                for i, p in enumerated_players
                if p.team == team
                and p.pos in defensive_pos
                or self.showdown
                and p.real_pos in defensive_pos
            ]

            for p in offensive_against:
                for d in defensive:
                    # For each combination of offensive player and their
                    # opposing defense, force no defense given offense (d <= 0)
                    self.solver.Add(d <= 1 - p)

    def _set_position_team_constraints(self):
        if self.position_per_team_rules:
            for team in self.teams:
                for rule in self.position_per_team_rules:
                    position_group_func, max_pos = rule
                    grouped_position_by_team = [
                        self.variables[i]
                        for i, p in self.enumerated_players
                        if p.team == team and position_group_func(p.pos)
                    ]
                    self.solver.Add(
                        max_pos >= self.solver.Sum(grouped_position_by_team)
                    )

    def _set_custom_rules(self):
        if self.custom_rules:
            for rule in self.custom_rules:
                group_a = [
                    self.variables[i]
                    for i, p in self.enumerated_players
                    if rule.group_a(p)
                ]
                group_b = [
                    self.variables[i]
                    for i, p in self.enumerated_players
                    if rule.group_b(p)
                ]
                self.solver.Add(
                    rule.comparison(self.solver.Sum, group_a, group_b)
                )

    def _set_positions(self):
        for position, min_limit, max_limit in self.position_limits:
            position_cap = self.solver.Constraint(min_limit, max_limit)

            for i, player in self.enumerated_players:
                if position == player.pos:
                    position_cap.SetCoefficient(self.variables[i], 1)

    def _set_general_positions(self):
        for (
            general_position,
            min_limit,
            max_limit,
        ) in self.general_position_limits:
            position_cap = self.solver.Constraint(min_limit, max_limit)

            for i, player in self.enumerated_players:
                if general_position == player.mlb_general_position:
                    position_cap.SetCoefficient(self.variables[i], 1)
                if general_position == player.nba_general_position:
                    position_cap.SetCoefficient(self.variables[i], 1)

    def _set_no_duplicate_lineups(self):
        for roster in self.existing_rosters:
            max_repeats = self.roster_size - 1
            if self.settings.uniques:
                max_repeats = max(self.roster_size - self.settings.uniques, 1)
            repeated_players = self.solver.Constraint(0, max_repeats)
            for player in roster.sorted_players():
                i = self.player_to_idx_map.get(player.solver_id)
                if i is not None:
                    repeated_players.SetCoefficient(self.variables[i], 1)

    def _set_min_teams(self):
        """
        Add constraints for maximum players on an individual team
        and total represented teams if applicable.

        For NHL, the min team restriction does not count
        goalies

        Ref: https://www.draftkings.com/help/rules/nhl
        """
        teams = []
        min_teams = self.min_teams

        if min_teams > 1:
            is_dk_nhl = self.rule_set == DK_NHL_RULE_SET
            for team in self.teams:
                if team:
                    team_var = self.solver.IntVar(0, 1, team)
                    teams.append(team_var)
                    players_on_team = [
                        self.variables[i]
                        for i, p in self.enumerated_players
                        if p.team == team
                        and (
                            not is_dk_nhl
                            or p.pos != 'G'
                        )
                    ]

                    # Constrain to individual team for all players
                    self.solver.Add(
                        team_var <= self.solver.Sum(players_on_team)
                    )
                    self.solver.Add(
                        self.max_players_per_team
                        >= self.solver.Sum(players_on_team)
                    )

        # If min matchups is more than or equal to min_teams,
        # this constraint is redundant
        # Ex given min matchups of two, there will always be two teams,
        # so adding this constraint is needless if data is good.
        # That said, keep constraint to spot check data.
        if len(teams) > 0:
            self.solver.Add(self.solver.Sum(teams) >= self.min_teams)

    def _set_min_matchups(self):
        """
        Add minimum required matchups in a lineup,
        generally two for classic sports
        """
        matchups = []
        if self.min_matchups and self.min_matchups > 1:
            for matchup in self.matchups:
                if matchup:
                    matchup_var = self.solver.IntVar(0, 1, matchup)
                    matchups.append(matchup_var)
                    players_in_matchup = [
                        self.variables[i]
                        for i, p in self.enumerated_players
                        if p.matchup == matchup
                    ]
                    # Constrain to individual matchup for all players
                    self.solver.Add(
                        matchup_var <= self.solver.Sum(players_in_matchup)
                    )

            self.solver.Add(self.solver.Sum(matchups) >= self.min_matchups)
