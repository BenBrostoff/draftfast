import csv
from .nba_upload import (
    map_pids,
    write_to_csv,
)
from draftfast.rules import DRAFT_KINGS, FAN_DUEL


class CSVUploader(object):

    def __init__(self, pid_file, upload_file='./upload.csv'):
        self.upload_file = upload_file
        self.pid_map = self._map_pids(pid_file)

    def _map_pids(self, pid_file):
        raise NotImplementedError('You must implement _map_pids')


class DraftKingsNBAUploader(CSVUploader):
    HEADERS = [
        'PG', 'SG', 'SF',
        'PF', 'C', 'G', 'F', 'UTIL'
    ]

    def write_rosters(self, rosters):
        with open(self.upload_file, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(self.HEADERS)
            for roster in rosters:
                write_to_csv(
                    writer=writer,
                    roster=roster,
                    player_map=self.pid_map,
                )

    def _map_pids(self, pid_file):
        return map_pids(pid_file, game=DRAFT_KINGS)


class DraftKingsNFLUploader(CSVUploader):
    pass


class FanDuelNBAUploader(CSVUploader):
    HEADERS = [
        'PG', 'PG', 'SG', 'SG', 'SF',
        'SF', 'PF', 'PF', 'C',
    ]

    def write_rosters(self, rosters):
        with open(self.upload_file, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(self.HEADERS)
            for roster in rosters:
                write_to_csv(
                    writer=writer,
                    roster=roster,
                    player_map=self.pid_map,
                    game=FAN_DUEL,
                )

    def _map_pids(self, pid_file):
        return map_pids(pid_file, game=FAN_DUEL)


class FanDuelNFLUploader(CSVUploader):
    pass
