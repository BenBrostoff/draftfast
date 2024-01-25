from typing import List
from ortools.linear_solver import pywraplp


class PlayerPoolSettings(object):
    def __init__(
        self,
        min_proj=None,
        max_proj=None,
        min_avg=None,
        max_avg=None,
        min_salary=None,
        max_salary=None,
        randomize=None,
    ):
        self.min_proj = min_proj
        self.max_proj = max_proj
        self.min_avg = min_avg
        self.max_avg = max_avg
        self.min_salary = min_salary
        self.max_salary = max_salary
        self.randomize = randomize

    def exist(self):
        return str(self) != "None"

    # TODO: format this like a proper repr(), i.e. <PlayerPoolSettings: ...>
    def __repr__(self):
        if not str(self):
            return "<PlayerPoolSettings: None>"
        else:
            return str(self)

    def __str__(self):
        lines = []
        if self.min_proj:
            lines.append("Min projection: {}".format(self.min_proj))
        if self.max_proj:
            lines.append("Max projection: {}".format(self.min_proj))
        if self.min_avg:
            lines.append("Min average: {}".format(self.min_proj))
        if self.max_avg:
            lines.append("Max average: {}".format(self.min_proj))
        if self.min_salary:
            lines.append("Min salary: {}".format(self.min_proj))
        if self.max_salary:
            lines.append("Max salary: {}".format(self.min_proj))
        if self.randomize:
            lines.append("Randomization factor: {}".format(self.min_proj))

        if len(lines):
            return "\n".join(lines)
        else:
            return "None"


def default_comparison(
    solver_sum: pywraplp.Solver.Sum,
    g_a: List[pywraplp.Variable],
    g_b: List[pywraplp.Variable],
) -> bool:
    """
    You will generally want to override this as the default
    assumes total players in group A plus one is less than or
    equal to total players in group B. While this may be true in
    some cases, it's not appropriate for all.

    Some other examples to help get started:

    Player A must be played with Player B:
    lambda sum, a, b: sum(a) == sum(b)

    Always have at least three of this group (A):
    lambda sum, a, b: sum(a) >= 3

    Never play this group (A):
    lambda sum, a, b: sum(a) <= 1
    """
    return solver_sum(g_a) + 1 <= solver_sum(g_b)


class CustomRule(object):
    def __init__(self, group_a, group_b, comparison=None):
        self.group_a = group_a
        self.group_b = group_b
        self.comparison = comparison or default_comparison

    def __repr__(self):
        import inspect as i

        return (
            f"{i.getsource(self.group_a)}"
            f"{i.getsource(self.group_b)}"
            f"{i.getsource(self.comparison)}"
        )


class OptimizerSettings(object):
    def __init__(
        self,
        stacks=None,
        existing_rosters=None,
        force_combo=None,
        combo_allow_te=None,
        uniques=None,
        no_offense_against_defense=False,
        no_defense_against_captain=False,
        showdown_teams=None,
        min_teams=2,
        min_matchups=None,
        custom_rules=None,
    ):
        """
        A note on defaults:

        min_teams 2 - this constraint is common across Classic and Showdown.
        Note that a ruleset cannot be override on min_teams and you
        must mutate the ruleset directly; this feature is to avoid
        modifying rules that would cause invalid lineups.

        - In Showdown, you must have two teams represented, although only
        one matchup exists to choose from.
        - In Classic, the constraint of two matchups
        forces a minimum of two teams

        Certain sports additionally impose
        max players per team constraints, which
        is not overridable outside of mutating RuleSets.
        """
        self.stacks = stacks
        self.existing_rosters = existing_rosters or []
        self.force_combo = force_combo
        self.combo_allow_te = combo_allow_te
        self.uniques = uniques
        self.no_offense_against_defense = no_offense_against_defense
        self.no_defense_against_captain = no_defense_against_captain
        self.showdown_teams = showdown_teams
        self.min_teams = min_teams
        self.min_matchups = min_matchups
        self.custom_rules = custom_rules

    # TODO: format this like a proper repr(), i.e. <OptimizerSettings: ...>
    def __repr__(self):
        if not str(self):
            return "<OptimizerSettings: None>"
        return str(self)

    def __str__(self):
        lines = []
        if self.stacks and len(self.stacks):
            lines.append(
                "Stacks: {}".format([(x.team, x.count) for x in self.stacks])
            )
        if self.no_offense_against_defense:
            lines.append(
                "No offense against D: {}".format(
                    self.no_offense_against_defense
                )
            )
        if self.custom_rules:
            lines.append("Custom rules: {}".format(self.custom_rules))

        if len(lines):
            return "\n".join(lines)
        else:
            return "None"


class UploadSettings(object):
    def __init__(self, pid_file, upload_file, rule_set, rosters):
        self.pid_file = pid_file
        self.upload_file = upload_file
        self.rule_set = rule_set
        self.rosters = rosters


class Stack(object):
    def __init__(
        self,
        team: str,
        count: int,
        stack_lock_pos=None,
        stack_eligible_pos=None,
    ):
        self.team = team
        self.count = count
        self.stack_lock_pos = stack_lock_pos
        self.stack_eligible_pos = stack_eligible_pos
