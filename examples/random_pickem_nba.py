"""
Generate as many random lineups as you want
for an NBA Pick'Em contest.

The output here is a CSV file that can be used
to upload lineups at https://www.draftkings.com/lineup/upload

Pre-reqs:
1) Salary file exists at passed location
2) Projection file exists at passed location
3) PIDS file downloaded from aforementioned location

Example usage:
```python
from examples import random_pickem_nba
random_pickem_nba.run(
    '~/Downloads/salaries-file.csv',
    '~/Downloads/pid-file.csv',
    10
)
```
"""

import random
from pickem import pickem_upload, pickem_optimize, pickem_orm


def run(pickem_file_location, map_file_location, lineup_nums=10):
    pickem_upload.create_upload_file()
    player_map = pickem_upload.map_pids(map_file_location)
    all_players = pickem_optimize.get_all_players(
        pickem_file_location,
        projection_file=None,
        use_averages=True,
    )

    for _ in range(lineup_nums):
        random_lineup = []
        for t in pickem_orm.TIERS:
            random_lineup.append(
                random.choice(
                    [p for p in all_players if p.tier == t]
                )
            )
        pickem_upload.update_upload_csv(
            player_map,
            pickem_orm.TieredLineup(random_lineup)
        )
