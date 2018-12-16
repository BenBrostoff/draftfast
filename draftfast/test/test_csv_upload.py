import os
import csv
from typing import Type
from nose.tools import assert_equal
from draftfast import rules
from draftfast import optimize
from draftfast.csv_parse import uploaders, salary_download


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


def test_dk_nba_upload():
    row = _get_first_written_row(
        game=rules.DRAFT_KINGS,
        salary_file_location='{}/data/dk-nba-salaries.csv'.format(CURRENT_DIR),
        rule_set=rules.DK_NBA_RULE_SET,
        pid_file='{}/data/dk-nba-pids.csv'.format(CURRENT_DIR),
        Uploader=uploaders.DraftKingsNBAUploader,
    )
    assert_equal(
        row,
        [
            '11743190',
            '11743146',
            '11743013',
            '11743007',
            '11743024',
            '11743176',
            '11743369',
            '11743142',
        ]
    )


def test_dk_el_upload():
    row = _get_first_written_row(
        game=rules.DRAFT_KINGS,
        salary_file_location='{}/data/dk-euro-league-salaries.csv'.format(
            CURRENT_DIR
        ),
        rule_set=rules.DK_EURO_LEAGUE_RULE_SET,
        pid_file='{}/data/dk-euro-league-pids.csv'.format(CURRENT_DIR),
        Uploader=uploaders.DraftKingsELUploader,
    )
    assert_equal(
        row,
        [
            '11799918',
            '11799942',
            '11799922',
            '11799956',
            '11800052',
            '11799950',
        ],
    )


def test_dk_soccer_upload():
    row = _get_first_written_row(
        game=rules.DRAFT_KINGS,
        salary_file_location='{}/data/dk-soccer-salaries.csv'.format(
            CURRENT_DIR
        ),
        rule_set=rules.DK_SOCCER_RULE_SET,
        pid_file='{}/data/dk-soccer-pids.csv'.format(CURRENT_DIR),
        Uploader=uploaders.DraftKingsSoccerUploader,
    )
    assert_equal(
        row,
        [
            '11801828',
            '11801837',
            '11801757',
            '11801761',
            '11801685',
            '11801733',
            '11801676',
            '11801778',
        ],
    )


def test_fd_nba_upload():
    row = _get_first_written_row(
        game=rules.FAN_DUEL,
        salary_file_location='{}/data/fd-nba-salaries.csv'.format(CURRENT_DIR),
        rule_set=rules.FD_NBA_RULE_SET,
        pid_file='{}/data/fd-nba-pids.csv'.format(CURRENT_DIR),
        Uploader=uploaders.FanDuelNBAUploader,
    )
    assert_equal(
        row,
        [
            '30803-9535:Kyle Lowry',
            '30803-9475:Derrick Rose',
            '30803-9714:DeMar DeRozan',
            '30803-40201:Dennis Schroder',
            '30803-9646:Kevin Durant',
            '30803-12341:Paul George',
            '30803-9957:Serge Ibaka',
            '30803-9874:Kevin Love',
            '30803-12362:DeMarcus Cousins',
        ]
    )


def _get_first_written_row(
        game: str,
        salary_file_location: str,
        rule_set: rules.RuleSet,
        pid_file: str,
        Uploader: Type[uploaders.CSVUploader],
) -> list:
    players = salary_download.generate_players_from_csvs(
        game=game,
        salary_file_location=salary_file_location,
    )
    roster = optimize.run(
        rule_set=rule_set,
        player_pool=players,
        verbose=True,
    )
    upload_file = '{}/data/current-upload.csv'.format(CURRENT_DIR)
    uploader = Uploader(
        pid_file=pid_file,
        upload_file=upload_file,
    )
    uploader.write_rosters([roster])

    row = None
    with open(upload_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for idx, row in enumerate(reader):
            if idx == 0:
                continue

    return row
