import os
import random
from draftfast.pickem.pickem_optimize import optimize
from draftfast.csv_parse import uploaders, salary_download
from draftfast import rules
from draftfast.lineup_constraints import LineupConstraints

salary_file_location = os.environ.get('PICKEM')
pid_file_location = os.environ.get('PICKEM_PIDS')


players = salary_download.generate_players_from_csvs(
    game=rules.DRAFT_KINGS,
    salary_file_location=salary_file_location,
    ruleset=rules.DK_NBA_PICKEM_RULE_SET,
)

rosters = []
for p in range(20):
    player = random.choice(players)
    roster = optimize(
        all_players=players,
        constraints=LineupConstraints(locked=[p.name]),
    )
    rosters.append(roster)

uploader = uploaders.DraftKingsNBAPickemUploader(
    pid_file=pid_file_location,
)


uploader.write_rosters(rosters)
