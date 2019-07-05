import csv
from .nba_upload import (
    map_pids,
    write_to_csv,
)
from draftfast.rules import DRAFT_KINGS, FAN_DUEL
from draftfast.pickem import pickem_orm, pickem_upload


class CSVUploader(object):

    def __init__(self, pid_file, upload_file='./upload.csv',
                 encoding='utf-8', errors='replace'):
        self.upload_file = upload_file
        self.encoding = encoding
        self.errors = errors
        self.pid_map = self._map_pids(pid_file)

    def _map_pids(self, pid_file):
        raise NotImplementedError('You must implement _map_pids')


class DraftKingsUploader(CSVUploader):
    def write_rosters(self, rosters):
        with open(self.upload_file, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(self.HEADERS)
            for roster in rosters:
                write_to_csv(
                    writer=writer,
                    roster=roster,
                    player_map=self.pid_map,
                    league=self.LEAGUE,
                )

    def _map_pids(self, pid_file):
        return map_pids(
            pid_file,
            game=DRAFT_KINGS,
            encoding=self.encoding,
            errors=self.errors,
        )


class DraftKingsNBAUploader(DraftKingsUploader):
    LEAGUE = 'NBA'
    HEADERS = [
        'PG', 'SG', 'SF',
        'PF', 'C', 'G', 'F', 'UTIL'
    ]


class DraftKingsELUploader(DraftKingsUploader):
    LEAGUE = 'EL'
    HEADERS = [
        'G', 'G', 'F', 'F', 'F', 'UTIL',
    ]


class DraftKingsSoccerUploader(DraftKingsUploader):
    LEAGUE = 'SOCCER'
    HEADERS = [
        'F', 'F', 'M', 'M', 'D', 'D', 'GK', 'UTIL',
    ]


class DraftKingsNHLUploader(DraftKingsUploader):
    LEAGUE = 'NHL'
    HEADERS = [
        'C', 'C', 'W', 'W', 'W', 'D',
        'D', 'G', 'UTIL',
    ]


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
        return map_pids(
            pid_file,
            game=FAN_DUEL,
            encoding=self.encoding,
            errors=self.errors,
        )


class FanDuelNFLUploader(CSVUploader):
    pass


class DraftKingsNBAPickemUploader(CSVUploader):
    def write_rosters(self, rosters):
        with open(self.upload_file, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=pickem_orm.TIERS)
            writer.writeheader()
            for roster in rosters:
                pickem_upload.write_to_csv(
                    writer=writer,
                    roster=roster,
                    player_map=self.pid_map,
                )

    def _map_pids(self, pid_file):
        return pickem_upload.map_pids(pid_file)


class DraftKingsCaptainShowdownUploader(DraftKingsUploader):
    HEADERS = [
        'CPT', 'UTIL', 'UTIL', 'UTIL', 'UTIL', 'UTIL'
    ]

    def write_rosters(self, rosters):
        with open(self.upload_file, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(self.HEADERS)
            for roster in rosters:
                writer.writerow([
                    p.get_player_id(self.pid_map)
                    for p in roster.sorted_players()
                ])
