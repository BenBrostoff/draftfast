import locale
from datetime import datetime, date
from terminaltables import AsciiTable
import numpy as np
import NFL_Draftkings as NFLDK

try:
    locale.setlocale(locale.LC_ALL, 'en_US')
except Exception:
    pass


def cs(n):
    return locale.format('%d', n, grouping=True)


def retrieve_all_players_from_history(args):
    from draft_kings_db import client
    c = client.DraftKingsHistory()

    all_players = []

    # TODO - remove and allow retrieval from DB
    historical_datetime = datetime.strptime(args.historical_date, '%Y-%m-%d')
    historical_date = date(
        historical_datetime.year,
        historical_datetime.month,
        historical_datetime.day
    )
    c.initialize_nba(from_date=historical_date, to_date=historical_date)

    for perf in c.lookup_nba_performances(date=historical_date, limit=None):
        for pos in perf.position.split('/'):
            all_players.append(
                Player(
                    pos,
                    perf.name,
                    perf.salary,
                    possible_positions=perf.position,
                    multi_position=('/' in perf.position),
                    team=perf.team,
                    matchup=perf.matchup,
                    lock=(args.locked and perf.name in args.locked),
                    proj=perf.draft_kings_points
                )
            )
    return all_players


class Roster:
    def __init__(self):
        self.players = []

    def __repr__(self):
        table_data = []
        headers = [
            'Position',
            'Player',
            'Team',
            'Matchup',
            'Salary',
            'Projection',
            'vs. Avg.',
            'Locked'
        ]
        table_data.append(headers)
        for p in self.sorted_players():
            table_data.append(p.to_table_row())

        table = AsciiTable(table_data).table

        aggregate_info = '\n\nProjected Score: {} \t Cost: ${}'.format(
            self.projected(),
            cs(self.spent()))

        source = '\nProjection Source: {}'.format(
            getattr(self, 'projection_source', None))

        return table + aggregate_info + source

    def __eq__(self, roster):
        if self.__class__ == roster.__class__ and \
           len(self.players) == 9 and len(roster.players) == 9:
            for p in self.players:
                if not any(filter(lambda x: x == p, roster.players)):
                    return False
            return True
        return False

    @property
    def projection_source(self):
        return self._source

    @projection_source.setter
    def projection_source(self, source):
        self._source = source

    def add_player(self, player):
        self.players.append(player)

    def spent(self):
        return sum(map(lambda x: x.cost, self.players))

    def projected(self):
        return sum(map(lambda x: x.proj, self.players))

    def position_order(self, player):
        return self.POSITION_ORDER[player.pos]

    def sorted_players(self):
        return sorted(
            self.players,
            key=lambda p: self.position_order(p)
        )


'''
POSITION_ORDER is based on the order
required by DraftKings' CSV download
'''


class NFLRoster(Roster):
    POSITION_ORDER = {
        'QB': 0,
        'RB': 1,
        'WR': 2,
        'TE': 3,
        'DST': 4
    }


class MLBRoster(Roster):
    POSITION_ORDER = {
        'P': 0,
        'SP': 0,
        'C': 1,
        '1B': 2,
        '2B': 3,
        '3B': 4,
        'SS': 5,
        'OF': 6,
        'RP': 7,
    }


class NBARoster(Roster):
    POSITION_ORDER = {
        'PG': 0,
        'SG': 1,
        'SF': 2,
        'PF': 3,
        'C': 4
    }


class WNBARoster(Roster):
    POSITION_ORDER = {
        'G': 0,
        'F': 1,
        'SG': 2,
        'SF': 3,
        'PF': 4,
    }


class NASCARRoster(Roster):
    POSITION_ORDER = {
        'D': 1,
    }


class PGARoster(Roster):
    POSITION_ORDER = {
        'G': 0,
    }

class RosterSelect:
    @staticmethod
    def roster_gen(league):
        roster_dict = {
            'NBA': NBARoster(),
            'WNBA': WNBARoster(),
            'NFL': NFLRoster(),
            'MLB': MLBRoster(),
            'PGA': PGARoster(),
            'NASCAR': NASCARRoster(),
        }
        return roster_dict[league]


class Player(object):
    _PLAYER_DATA_CACHE = {}

    def __init__(
        self,
        pos,
        name,
        cost,
        proj=0,
        projected_ownership_pct=0,
        lineup_count=0,
        average_score=0,
        matchup=None,
        team=None,
        marked=None,
        possible_positions=None,
        lock=False,
        multi_position=False
    ):
        self.pos = pos
        self.name = name
        self.cost = float(cost)
        self.team = team
        self.matchup = matchup
        self.proj = proj
        self.average_score = average_score
        self.projected_ownership_pct = projected_ownership_pct
        self.lineup_count = lineup_count
        self.marked = marked
        self.lock = lock
        self.multi_position = multi_position
        self.possible_positions = possible_positions

    def get_player_id(self, player_map):
        return player_map[self.name + ' ' + self.possible_positions]

    def to_table_row(self):
        return [
            self.formatted_position,
            self.name,
            self.team,
            self.matchup,
            cs(self.cost),
            self.proj,
            self.__format_v_avg(),
            'LOCK' if self.lock else ''
        ]

    def __repr__(self):
        v_avg = self.__format_v_avg()
        player_dict = dict(
            pos=self.formatted_position,
            name=self.name,
            team=self.team,
            match=self.matchup,
            cost=cs(self.cost),
            proj=self.proj,
            v_avg=v_avg,
            lock='LOCK' if self.lock else ''
        )

        return "[{pos: <2}] {name: <20} {team} {match} " \
               "(${cost}, {proj} ({v_avg})), {lock}".format(
                **player_dict)

    def __eq__(self, player):
        return self.pos == player.pos and \
               self.name == player.name and \
               self.cost == player.cost and \
               self.team == player.team

    @property
    def value(self):
        return round(self.proj / (self.cost / 1000), 2)

    @property
    def solver_id(self):
        return '{} {} {}'.format(self.name, self.pos, self.team)

    @property
    def formatted_position(self):
        if self.multi_position:
            return '{} ({})'.format(self.possible_positions, self.pos)
        return self.pos

    @property
    def v_avg(self):
        return self.proj - self.average_score

    @property
    def is_home(self):
        match_up_teams = self.matchup.split(' ')[0]
        return self.team == match_up_teams.split('@')[-1]

    @property
    def nba_general_position(self):
        if self.pos == 'SG' or self.pos == 'PG' or self.pos == 'G':
            return 'G'
        elif self.pos == 'SF' or self.pos == 'PF' or self.pos == 'F':
            return 'F'
        return 'C'

    def set_historical(self, week, season):
        if self.name in self._PLAYER_DATA_CACHE:
            self.__set_from_data_cache(
                self._PLAYER_DATA_CACHE[self.name])
            return
        try:
            scores = NFLDK.get_weekly_scores(
                name=self.name,
                weeks=range(1, week),
                season=season
            )
            scores = [
                s.get('stats', 0) for s in scores
            ]
            self.all_scores = scores
            self.last_score = scores[-1]
            self.max_score = max(scores)
            self.min_score = min(scores)
            self.average_score = min(scores)
            self.median_score = np.median(scores)
            self.stdev_score = np.std(scores)

            self.__set_data_cache()

            print('Fetched player data for {}'.format(self.name))
        except Exception:
            self._PLAYER_DATA_CACHE[self.name] = None
            print('Failed to fetch player data for {}'.format(self.name))

    def __set_data_cache(self):
        self._PLAYER_DATA_CACHE[self.name] = {
            'all_scores': self.all_scores,
            'last_score': self.last_score,
            'max_score': self.max_score,
            'min_score': self.min_score,
            'average_score': self.average_score,
            'median_score': self.median_score,
            'std_score': self.stdev_score,
        }

    def __set_from_data_cache(self, player_data):
        if player_data is None:
            return
        for k, v in player_data.items():
            setattr(self, k, v)

    def __format_v_avg(self):
        if self.v_avg > 0:
            return '\x1b[0;32;40m{}\x1b[0m'.format(self.v_avg)
        return '\x1b[0;31;40m{}\x1b[0m'.format(self.v_avg)


class Game:
    def __init__(self, team, opp):
        self.team = team
        self.opponent = opp

    def __repr__(self):
        return '{} @ {}'.format(self.team, self.opponent)

    def team_in_game(self, team):
        return team == self.team or team == self.opponent

    def get_teams(self):
        return self.team, self.opponent
