import csv
from .nba_upload import (
    map_pids as dk_nba_map_pids,
    write_to_csv as dk_nba_write_to_csv,
)


class CSVUploader(object):

    def __init__(self, pid_file, upload_file='./upload.csv'):
        self.upload_file = upload_file
        self.pid_map = self._map_pids(pid_file)

    def _map_pids(self, pid_file):
        raise NotImplementedError('You must implement map_pids')


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
                dk_nba_write_to_csv(
                    writer=writer,
                    roster=roster,
                    player_map=self.pid_map,
                )

    def _map_pids(self, pid_file):
        return dk_nba_map_pids(pid_file)


class DraftKingsNFLUploader(CSVUploader):
    pass


class FanDuelNBAUploader(CSVUploader):
    pass


class FanDuelNFLUploader(CSVUploader):
    pass
