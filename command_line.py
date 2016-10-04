import argparse


OPTIMIZE_COMMAND_LINE = [
    ['-s', 'scrape from FanPros', 'y'],
    ['-mp', 'missing players to allow', 100],
    ['-sp', 'salary threshold to ignore', 3000],
    ['-ms', 'max salary for player on roster', 10000],
    ['-i', 'iterations to run', 3],
    ['-lp', 'lowest acceptable projection', 0],
    ['-po', 'highest acceptable ownership', 100],
    ['-limit', 'disallow more than 1 player per team sans QB', 'n'],
    ['-duo', 'force a QB + WR/TE duo on specific team', 'n'],
    ['-teams', 'player must be on specified teams', None],
    ['-locked', 'player must be in final lineup', None],
    ['-banned', 'player cannot be named players', None],
    ['-dtype', 'specify WR or TE in combo', 'wr'],
    ['-source', 'data source to use', 'fanpros'],
    ['-l', 'league', 'NFL'],
    ['-pids', 'Player id file (create upload file)', None],
    ['-keep_pids', 'Player id file (create upload file)', None],
    ['-po_location', 'Projected ownership percentages file location', None]
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
