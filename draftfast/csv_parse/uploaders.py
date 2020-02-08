import csv
from itertools import islice
from .upload import (
    write_to_csv,
)
from draftfast.rules import DRAFT_KINGS, FAN_DUEL
from draftfast.pickem import pickem_orm, pickem_upload
from draftfast import dke_exceptions as dke

NAME_MAP = {
    DRAFT_KINGS: {
        'start': 'TeamAbbrev',
        'name': 'Name',
        'position': 'Position',
        'id': 'ID',
    },
    FAN_DUEL: {
        'start': '"Nickname"',
        'name': '"Nickname"',
        'position': '"Position"',
        'id': '"Player ID + Player Name"',
    },
}


def map_pids(pid_file, encoding, errors, game=DRAFT_KINGS):
    start = NAME_MAP.get(game).get('start')
    name = NAME_MAP.get(game).get('name')
    position = NAME_MAP.get(game).get('position')
    p_id = NAME_MAP.get(game).get('id')

    player_map = {}
    with open(pid_file, 'r') as f:
        n = 0
        fields = None
        for line in f.readlines():
            n += 1
            if start in line:  # line with field names was found
                fields = line.split(',')
                break

        if not fields:
            raise dke.InvalidCSVUploadFileException(
                "Check that you're using the DK CSV upload template, " +
                "which can be found at " +
                "https://www.draftkings.com/lineup/upload.")

        f.close()
        f = islice(open(pid_file, 'r',
                        encoding=encoding, errors=errors), n, None)
        reader = csv.DictReader(f, fieldnames=fields)
        for line in reader:
            # DraftKings adds spaces to DST for NFL
            if 'DST' in line[position]:
                line[name] = line[name].strip()
                line[position] = line[position].strip()

            player_map[line[name] + " " + line[position]] = line[p_id]

    return player_map


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


class DraftKingsNFLUploader(DraftKingsUploader):
    LEAGUE = 'NFL'
    HEADERS = [
        'QB', 'RB', 'RB',
        'WR', 'WR', 'WR',
        'TE', 'FLEX', 'DST'
    ]


class DraftKingsXFLUploader(DraftKingsUploader):
    LEAGUE = 'XFL'
    HEADERS = [
        'QB', 'RB',
        'WR', 'WR',
        'FLEX', 'FLEX',
        'DST',
    ]


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
