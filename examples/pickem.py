import random
import os
from draftfast.pickem_optimize import get_all_players, optimize
from draftfast.csv_parse import uploaders
from draftfast.settings import PickemSettings


players = get_all_players(
    pickem_file_location=os.environ.get('PICKEM'),
)
rosters = []

player = random.choice(players)
for _ in range(20):
    rosters.append(optimize(
        all_players=players,
        pickem_settings=PickemSettings(locked=[player.name]))
    )

uploader = uploaders.DraftKingsNBAPickemUploader(
    pid_file=os.environ.get('PICKEM_PIDS'),
)
uploader.write_rosters(rosters)
