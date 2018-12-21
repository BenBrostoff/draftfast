from nose import tools as ntools
from draftfast.settings import PickemSettings
from draftfast.pickem_optimize import get_all_players, optimize
from draftfast.csv_parse import uploaders


def test_upload():
    players = get_all_players(
        pickem_file_location='',
    )
    rosters =[optimize(
        all_players=players,
    )]
    uploader = uploaders.DraftKingsNBAPickemUploader(
        pid_file='',
    )
    uploader.write_rosters(rosters)
