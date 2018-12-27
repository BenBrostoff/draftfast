import argparse
import os

OPTIMIZE_COMMAND_LINE = [
    ['-use_averages', 'use averages as projections', False],
    ['-v_avg', 'projections must be within points v avg', 100000],
    ['-min_avg', 'player must exceed average points', 0],
    ['-lp', 'lowest acceptable projection', 0],
    ['-home', 'only select players playing at home', None],
    ['-locked_teams', 'player must be on specified teams', None],
    ['-banned_teams', 'player must not be on specified teams', None],
    ['-source', 'data source to use', 'nfl_rotogrinders'],
    ['-pids', 'player id file (create upload file)', None],
    ['-keep_pids', 'Keep current upload file', None],
    ['-salary_file', 'file location for salaries',
     os.getcwd() + '/data/current-salaries.csv'],
    ['-projection_file', 'file location for projections',
     os.getcwd() + '/data/current-projections.csv'],
    ['-randomize_projections', 'use random projection factor', None],
]


MULTIPLE_ARGS_COMMAND = [
    '-teams',
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
            default=opt[2]
        )
    return PARSER.parse_args()
