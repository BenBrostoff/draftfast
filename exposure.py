import math
import csv
import random
from collections import OrderedDict
from terminaltables import AsciiTable

# TODO use exposure objects

def parse_exposure_file(file_location):
    """
    :param file: File location
    :return: Dictionary of exposures
    { <name>: { min: <min>, max: <max> } }
    """
    exposures = []
    with open(file_location, 'r') as filename:
        reader = csv.DictReader(filename)
        for row in reader:
            if 'name' not in row or \
               'min' not in row or \
               'max' not in row:
                raise Exception('''
                    You must provide a min, max and name
                    for each row - got {}.
                    '''.format(row)
                )
            exposures.append({
                'name': row['name'],
                'min': float(row['min']),
                'max': float(row['max']),
            })

    return exposures


def get_exposure_args(existing_rosters, exposure_bounds, N, use_random,
                      random_seed):
    exposures = {}
    for r in existing_rosters:
        for p in r.players:
            exposures[p.name] = exposures.get(p.name, 0) + 1

    if use_random == 'y':
        return get_exposure_args_random(exposures, existing_rosters,
                                        exposure_bounds, N, random_seed)

    return get_exposure_args_deterministic(exposures, existing_rosters,
                                           exposure_bounds)


def get_exposure_args_deterministic(exposures, existing_rosters,
                                    exposure_bounds):
    banned = []
    locked = []

    for bound in exposure_bounds:
        name = bound['name']

        total = float(len(existing_rosters) + 1)
        min_lines = bound['min'] * total
        max_lines = math.floor(bound['max'] * total)
        lineups = exposures.get(name, 0)

        if lineups < min_lines:
            # TODO - downsize locked so solution is not impossible
            locked.append(name)
        elif lineups >= max_lines:
            banned.append(name)

    return {
        'banned': banned,
        'locked': locked,
    }


def get_exposure_args_random(exposures, existing_rosters, exposure_bounds, N,
                             random_seed):
    random.seed(random_seed)

    banned = []
    locked = []

    for bound in exposure_bounds:
        name = bound['name']

        # exclude players who have met max exposure
        if exposures.get(name, 0) >= N * bound['max']:
            banned.append(name)
            continue

        # ramdomly lock in players based on the desired exposure
        # TODO - downsize locked so solution is not impossible
        if random.random() <= bound['max']:
            locked.append(name)

    return {
        'banned': banned,
        'locked': locked,
    }


def check_exposure(rosters, bounds):
    if not bounds:
        return {}

    exposures = {}
    for r in rosters:
        for p in r.players:
            exposures[p.name] = exposures.get(p.name, 0) + 1

    exposure_diffs = {}

    for bound in bounds:
        name = bound['name']
        exposure = exposures.get(name, 0)

        if exposure > len(rosters) * bound['max']:
            exposure_diffs[name] = exposure - len(rosters) * bound['max']
        elif exposure < len(rosters) * bound['min']:
            exposure_diffs[name] = exposure - len(rosters) * bound['min']

    return exposure_diffs


def get_exposure_table(rosters, bounds):
    exposures = {}
    players = {}
    for r in rosters:
        for p in r.players:
            exposures[p.name] = exposures.get(p.name, 0) + 1
            players[p.name] = p

    exposures = OrderedDict(sorted(exposures.items(),
                                   key=lambda t: t[1],
                                   reverse=True))

    table_data = []
    headers = [
        'Position',
        'Player',
        'Team',
        'Matchup',
        'Salary',
        '# Lineups',
        'Min',
        'Max'
    ]
    table_data.append(headers)

    for name, num in exposures.items():

        s_min = ''
        s_max = ''

        # TODO format min/max as a single string
        if bounds:
            for bound in bounds:
                if bound['name'] == name:
                    s_min = len(rosters) * bound['min']
                    s_max = len(rosters) * bound['max']
                    if num > len(rosters) * bound['max']:
                        s_min = '\x1b[0;31;40m{:0.2f}\x1b[0m'.format(
                                    len(rosters) * bound['max']
                                    )
                    elif num < len(rosters) * bound['min']:
                        s_max = '\x1b[0;31;40m{:0.2f}\x1b[0m'.format(
                                    len(rosters) * bound['min']
                                    )

                    continue

        table_data.append(players[name].to_exposure_table_row(num,
                                                              s_min,
                                                              s_max))

    table = AsciiTable(table_data)
    table.justify_columns[4] = 'right'
    table.justify_columns[5] = 'right'
    table.justify_columns[6] = 'right'
    table.justify_columns[7] = 'right'

    return 'Roster Exposure:\n' + table.table
