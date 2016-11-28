import argparse


OPTIMIZE_COMMAND_LINE = [
    ['-s', 'scrape from data source', 'y'],
    ['-w', 'current week', None],
    ['-season', 'current season', None],
    ['-historical', 'fetch historical data', 'n'],
    ['-mp', 'missing players to allow', 100],
    ['-sp', 'salary threshold to ignore', 3000],
    ['-ms', 'max salary for player on roster', 100000],
    ['-v_avg', 'projections must be within points v avg', 100000],
    ['-i', 'iterations to run', 3],
    ['-lp', 'lowest acceptable projection', 0],
    ['-po', 'highest acceptable ownership', 100],
    ['-limit', 'disallow more than 1 player per team sans QB', 'n'],
    ['-home', 'only select players playing at home', None],
    ['-duo', 'force a QB + WR/TE duo on specific team', 'n'],
    ['-no_double_te', 'disallow two tight end lineups', 'n'],
    ['-teams', 'player must be on specified teams', None],
    ['-locked', 'player must be in final lineup', None],
    ['-banned', 'player cannot be named players', None],
    ['-dtype', 'specify WR or TE in combo', 'wr'],
    ['-source', 'data source to use', 'nfl_rotogrinders'],
    ['-l', 'league', 'NFL'],
    ['-pids', 'Player id file (create upload file)', None],
    ['-keep_pids', 'Keep current upload file', None],
    ['-po_location', 'Projected ownership percentages file location', None],
    ['test_mode', 'Run in test mode', False],
]


MULTIPLE_ARGS_COMMAND = [
    '-teams',
    '-banned',
    '-locked'
]

PARSER = argparse.ArgumentParser()


def get_args():
    for opt in OPTIMIZE_COMMAND_LINE:
        nargs = '?'
        if opt[0] in MULTIPLE_ARGS_COMMAND:
            nargs = '+'
        PARSER.add_argument(
            opt[0],
            nargs=nargs,
            help=opt[1],
            default=opt[2])
    return PARSER.parse_args()
