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

class OptimizerSettings(object):

    def __init__(self):
        pass


class UploadSettings(object):

    def __init__(self, pid_file, upload_file,
                 rule_set, rosters):
        self.pid_file = pid_file
        self.upload_file = upload_file
        self.rule_set = rule_set
        self.rosters = rosters