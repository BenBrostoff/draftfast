from os import environ
from draftfast import rules
from draftfast.optimize import run_multi
from draftfast.csv_parse import salary_download, uploaders

"""
Script to create 20 NBA lineups for DraftKings.

Assumptions:
- Environment variable called "downloads" has path to downloads
- In downloads, salary, projection and player ID files exist with
  the filenames listed in the script.
"""
downloads = environ.get('downloads')
players = salary_download.generate_players_from_csvs(
    salary_file_location='{}/NBA_SALS.csv'.format(downloads),
    projection_file_location='{}/NBA_PROJECTIONS.csv'.format(downloads),
    game=rules.DRAFT_KINGS,
)

rosters, _ = run_multi(
    iterations=20,
    exposure_bounds=[
        {
            'name': 'Damian Lillard',
            'min': 0.3,
            'max': 0.5,
        },
        {
            'name': 'LaMarcus Aldridge',
            'min': 0.5,
            'max': 0.7,
        },
    ],
    rule_set=rules.DK_NBA_RULE_SET,
    player_pool=players,
    verbose=True,
)

uploader = uploaders.DraftKingsNBAUploader(
    pid_file='{}/NBA_PIDS.csv'.format(downloads),
)
uploader.write_rosters(rosters)