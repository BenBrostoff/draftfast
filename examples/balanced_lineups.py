"""
Generate as many lineups as you want with
max exposures of your selected exposure to any one player.
The output here is a CSV file that can be used
to upload lineups at https://www.draftkings.com/lineup/upload

Pre-reqs:
1) Salary file exists at passed location
2) Projection file exists at passed location
3) PIDS file downloaded from aforementioned location

Example usage:
```python
from examples import balanced_lineups
balanced_lineups.run()
```
"""

import random
from collections import Counter
from optimize import run as optimizer_run
from argparse import Namespace

from csv_upload.nfl_upload import (
    update_upload_csv,
    create_upload_file,
    map_pids,
)
from csv_upload.nba_upload import (
    update_upload_csv,
    create_upload_file,
    map_pids,
)

DEFAULT_ARGS = dict(
    dtype='wr',
    duo='n',
    s='n',
    w=5,
    season=2017,
    historical='n',
    i=1,
    l='NBA',
    limit='n',
    no_double_te='y',
    lp=0,
    mp=500,
    ms=100000,
    sp=1000,
    banned=['Zach Randolph'],
    po=0,
    pids='data/pid-file.csv',
    salary_file='data/current-salaries.csv',
    projection_file='data/current-projections.csv',
    home='n',
    v_avg=100,
    source=None,
    locked=None,
    teams=None,
    po_location=None,
    flex_position=None,
)


def is_duplicate(r, rp):
    '''
    Checks for duplicate rosters irrespective of position distirbution.
    '''
    rp = [sorted([p.name for p in rn.players]) for rn in rp]
    rcur = sorted([p.name for p in r.players])
    return rcur in rp


def run(lineups=20, exposure=0.3):
    roster_list, player_list = [], []
    create_upload_file()
    player_map = map_pids(DEFAULT_ARGS['pids'])
    max_exposure = lineups * exposure
    exposure = None

    for _ in range(lineups):
        args = DEFAULT_ARGS.copy()
        if exposure:
            args['banned'] = DEFAULT_ARGS['banned'] + [
                name for name, freq in exposure.items()
                if freq > max_exposure
            ]
        roster = optimizer_run('NBA', [], Namespace(**args))

        # discard and replace duplicate lineups
        if is_duplicate(roster, roster_list):
            while is_duplicate(roster, roster_list):
                args['banned'].append(
                    random.choice(roster.players).name
                )
                roster = optimizer_run('NBA', [], Namespace(**args))

        roster_list.append(roster)
        player_list += [p.name for p in roster.players]

        update_upload_csv(
            player_map,
            roster.sorted_players()[:]
        )
        exposure = Counter(player_list)

    unique = len(set([str(r.players) for r in roster_list]))
    if unique != lineups:
        raise Exception(
            'Duplication error in logic. Expected {} and got {} lineups'
            .format(lineups, unique)
        )
