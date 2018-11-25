"""
Generate as many lineups as you want with
max exposures of your selected exposure to any one player,
with a specified minimum average of your choice.
The output here is a CSV file that can be used
to upload lineups at https://www.draftkings.com/lineup/upload

Pre-reqs:
1) Salary file exists at passed location
2) Projection file exists at passed location
3) PIDS file downloaded from aforementioned location

Example usage:
```python
from examples import balanced_lineups_mlb
balanced_lineups_mlb.run()
```
"""

import random
import numpy
from collections import Counter
from draftfast.optimize import run as optimizer_run
from argparse import Namespace

from draftfast.csv_parse import (
    update_upload_csv,
    create_upload_file,
    map_pids,
)

DEFAULT_ARGS = dict(
    s='n',
    w=5,
    i=1,
    league='MLB',
    limit='n',
    lp=0,
    mp=1000,
    ms=100000,
    sp=1000,
    banned=[],
    po=0,
    pids='data/pid-file-mlb.csv',
    salary_file='data/current-salaries.csv',
    projection_file='data/current-projections.csv',
    historical_date=None,
    home=None,
    v_avg=100,
    source='mlb_rotogrinders',
    no_double_te=None,
    season=None,
    flex_position=None,
    locked=None,
    teams=None,
    po_location=None,
    min_avg=None,
)


def is_duplicate(r, rp):
    '''
    Checks for duplicate rosters irrespective of position distribution.
    '''
    rp = [sorted([p.name for p in rn.players]) for rn in rp]
    rcur = sorted([p.name for p in r.players])
    return rcur in rp


def run(lineups=20, exposure=0.4, min_avg=1):
    DEFAULT_ARGS['min_avg'] = min_avg
    roster_list, player_list = [], []
    create_upload_file()
    player_map = map_pids(DEFAULT_ARGS['pids'])
    max_exposure = lineups * exposure
    exposure = None

    for _ in range(lineups):
        args = DEFAULT_ARGS.copy()
        if exposure:
            args['banned'] = DEFAULT_ARGS['banned'] + [
                name for name, freq in list(exposure.items())
                if freq > max_exposure
            ]
        roster = optimizer_run('MLB', [], Namespace(**args))

        # discard and replace duplicate lineups
        if is_duplicate(roster, roster_list):
            while is_duplicate(roster, roster_list):
                args['banned'].append(
                    random.choice(roster.players).name
                )
                roster = optimizer_run('NBA', [], Namespace(**args))

        roster_list.append(roster)
        player_list += [p.name for p in roster.players]

        update_upload_csv(player_map, roster)
        exposure = Counter(player_list)

    unique = len(set([str(r.players) for r in roster_list]))
    if unique != lineups:
        raise Exception(
            'Duplication error in logic. Expected {} and got {} lineups'
            .format(lineups, unique)
        )

    scores = [r.projected() for r in roster_list]
    print('Generated {} lineups.'.format(lineups))
    print('Maximum score: {}'.format(numpy.max(scores)))
    print('Minimum score: {}'.format(numpy.min(scores)))
    print('Average score: {}'.format(numpy.average(scores)))
    print('Median score: {}'.format(numpy.median(scores)))
