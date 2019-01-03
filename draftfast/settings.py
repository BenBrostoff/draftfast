# OPTIMIZE_COMMAND_LINE = [
#     ['-game', 'game to play', 'draftkings'],
#     ['-w', 'current week', None],
#     ['-season', 'current season', None],
#     [
#         '-historical_date',
#         'day from history to optimize on (use YYYY-MM-DD)',
#         None
#     ],
#     ['-mp', 'missing players to allow', 100],
#     ['-sp', 'salary threshold to ignore', 0],
#     ['-ms', 'max salary for player on roster', 100000],
#     ['-v_avg', 'projections must be within points v avg', 100000],
#     ['-i', 'iterations to run', 1],
#     ['-lp', 'lowest acceptable projection', 0],
#     ['-po', 'highest acceptable ownership', 100],
#     ['-limit', 'disallow more than 1 player per team sans QB', 'n'],
#     ['-home', 'only select players playing at home', None],
#     ['-no_double_te', 'disallow two tight end lineups', 'n'],
#     ['-teams', 'player must be on specified teams', None],
#     ['-locked', 'player must be in final lineup', None],
#     ['-banned', 'player cannot be named players', None],
#     ['-league', 'league', 'NFL'],
#     ['-pids', 'player id file (create upload file)', None],
#     ['-keep_pids', 'Keep current upload file', None],
#     ['-po_location', 'projected ownership percentages file location', None],
#     ['-salary_file', 'file location for salaries',
#      os.getcwd() + '/data/current-salaries.csv'],
#     ['-projection_file', 'file location for projections',
#      os.getcwd() + '/data/current-projections.csv'],
#     ['-flex_position', 'force player to have FLEX position', None],
#     ['-randomize_projections', 'use random projection factor', None],
#     ['-min_avg', 'player must exceed average points', None],
#     ['-use_average', 'Use player averages for projections', False],
#     ['-stack', 'Team to stack', None],
#     ['-stack_count', 'Total players to stack', 4],
#     ['-force_combo', 'Force a WR and QB combo', None],
#     ['-combo_allow_te', 'Allow TE in combo', None],
# ]


class PlayerPoolSettings(object):

    def __init__(self, min_proj=None, max_proj=None,
                 min_avg=None, max_avg=None, min_salary=None,
                 max_salary=None, randomize=None):
        self.min_proj = min_proj
        self.max_proj = max_proj
        self.min_avg = min_avg
        self.max_avg = max_avg
        self.min_salary = min_salary
        self.max_salary = max_salary
        self.randomize = randomize

    # TODO: format this like a proper repr(), i.e. <PlayerPoolSettings: ...>
    def __repr__(self):
        if not str(self):
            return '<PlayerPoolSettings: None>'
        else:
            return str(self)

    def __str__(self):
        lines = []
        if self.min_proj:
            lines.append('Min projection: {}'.format(self.min_proj))
        if self.max_proj:
            lines.append('Max projection: {}'.format(self.min_proj))
        if self.min_avg:
            lines.append('Min average: {}'.format(self.min_proj))
        if self.max_avg:
            lines.append('Max average: {}'.format(self.min_proj))
        if self.min_salary:
            lines.append('Min salary: {}'.format(self.min_proj))
        if self.max_salary:
            lines.append('Max salary: {}'.format(self.min_proj))
        if self.randomize:
            lines.append('Randomization factor: {}'.format(self.min_proj))

        if len(lines):
            return '\n'.join(lines)
        else:
            return 'None'


class OptimizerSettings(object):

    def __init__(self,
                 stacks=None,
                 existing_rosters=None, force_combo=None,
                 combo_allow_te=None, uniques=None,
                 no_offense_against_defense=False,
                 no_defense_against_captain=False,
                 showdown_teams=None,
                 min_teams=2):
        self.stacks = stacks
        self.existing_rosters = existing_rosters or []
        self.force_combo = force_combo
        self.combo_allow_te = combo_allow_te
        self.uniques = uniques
        self.no_offense_against_defense = no_offense_against_defense
        self.no_defense_against_captain = no_defense_against_captain
        self.showdown_teams = showdown_teams
        self.min_teams = min_teams

    # TODO: format this like a proper repr(), i.e. <OptimizerSettings: ...>
    def __repr__(self):
        if not str(self):
            return '<OptimizerSettings: None>'
        else:
            return str(self)

    def __str__(self):
        lines = []
        if self.stacks and len(self.stacks):
            lines.append('Stacks: {}'.format(
                        [(x.team, x.count) for x in self.stacks]
                    )
                )
        if self.min_teams:
            lines.append('Min teams: {}'.format(self.min_teams))
        if self.no_offense_against_defense:
            lines.append('No offense against D: {}'.format(
                    self.no_offense_against_defense
                )
            )

        if len(lines):
            return '\n'.join(lines)
        else:
            return 'None'


class UploadSettings(object):

    def __init__(self, pid_file, upload_file,
                 rule_set, rosters):
        self.pid_file = pid_file
        self.upload_file = upload_file
        self.rule_set = rule_set
        self.rosters = rosters


class Stack(object):
    def __init__(self, team: str, count: int):
        self.team = team
        self.count = count
