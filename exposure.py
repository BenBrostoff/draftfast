import math
import csv
from collections import Counter

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


def get_exposure_args(existing_rosters, exposure_bounds):
    names = []
    for r in existing_rosters:
        for p in r.players:
            names.append(p.name)

    banned = []
    locked = []
    exposures = Counter(names)
    exposure_dict = {}
    for name, total in exposures.items():
        exposure_dict[name] = total

    for bound in exposure_bounds:
        name = bound['name']

        total = float(len(existing_rosters) + 1)
        min_lines = bound['min'] * total
        max_lines = math.floor(bound['max'] * total)
        lineups = exposure_dict.get(name, 0)

        if lineups < min_lines:
            # TODO - downsize locked so solution is not impossible
            locked.append(name)
        elif lineups >= max_lines:
            banned.append(name)

    return {
        'banned': banned,
        'locked': locked,
    }