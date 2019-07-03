import locale
from terminaltables import AsciiTable
from functools import total_ordering
import re

try:
    locale.setlocale(locale.LC_ALL, 'en_US')
except Exception:
    pass


def cs(n):
    return locale.format('%d', n, grouping=True)


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

        table = AsciiTable(table_data)
        table.justify_columns[4] = 'right'
        table.justify_columns[5] = 'right'
        table.justify_columns[6] = 'right'

        aggregate_info = '\n\nProjected Score: {:0.2f} \t Cost: ${}'.format(
            self.projected(),
            cs(self.spent()))

        return table.table + aggregate_info

    def __eq__(self, roster):
        if not roster:
            return False

        player_set_a = set(a.solver_id for a in self.players)
        player_set_b = set(b.solver_id for b in roster.players)
        return player_set_a == player_set_b

    def __contains__(self, player):
        if isinstance(player, str):
            for p in self.players:
                if p.name == player or p.short_name == player:
                    return True
        elif isinstance(player, Player):
            return player in self.players
        else:
            raise NotImplementedError

        return False

    def exact_equal(self, roster):
        if not roster:
            return False

        player_set_a = [a.solver_id for a in self.sorted_players()]
        player_set_b = [b.solver_id for b in roster.sorted_players()]
        return player_set_a == player_set_b

    def add_player(self, player):
        self.players.append(player)

    def spent(self):
        return sum([x.cost for x in self.players])

    def projected(self):
        return sum([x.proj for x in self.players])

    def position_order(self, player):
        # raises exception in case someone tries to instantiate base class
        position_order = getattr(self, 'POSITION_ORDER')

        # default sort order is low->high, so use the negative of cost
        return position_order[player.pos], -player.cost

    def sorted_players(self):
        return sorted(
            self.players,
            key=lambda p: self.position_order(p)
        )


'''
POSITION_ORDER is based on the order
required by DraftKings' CSV download
'''


class ShowdownRoster(Roster):
    POSITION_ORDER = {
        'CPT': 0,
        'FLEX': 1,
    }


class NFLRoster(Roster):
    POSITION_ORDER = {
        'QB': 0,
        'RB': 1,
        'WR': 2,
        'TE': 3,
        'DST': 4,
        'D': 5,
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
        'D': 0,
    }


class PGARoster(Roster):
    POSITION_ORDER = {
        'G': 0,
    }


class SoccerRoster(Roster):
    POSITION_ORDER = {
        'F': 0,
        'M': 1,
        'D': 2,
        'GK': 3,
    }


class ELRoster(Roster):
    POSITION_ORDER = {
        'G': 0,
        'F': 1,
    }


class NHLRoster(Roster):
    POSITION_ORDER = {
        'C': 0,
        'W': 1,
        'D': 2,
        'G': 3,
    }


class RosterSelect:
    @staticmethod
    def roster_gen(league):
        roster_dict = {
            'NBA': NBARoster(),
            'NBA_SHOWDOWN': ShowdownRoster(),
            'WNBA': WNBARoster(),
            'NFL': NFLRoster(),
            'NFL_SHOWDOWN': ShowdownRoster(),
            'NFL_MVP': ShowdownRoster(),
            'MLB': MLBRoster(),
            'PGA': PGARoster(),
            'NASCAR': NASCARRoster(),
            'SOCCER': SoccerRoster(),
            'EL': ELRoster(),
            'NHL': NHLRoster(),
            'NHL_SHOWDOWN': ShowdownRoster(),
            'MLB_SHOWDOWN': ShowdownRoster(),
        }
        return roster_dict[league]


@total_ordering
class Player(object):
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
        position_lock=False,
        ban=False,
        multi_position=False,
    ):
        self.pos = pos
        self.name = name
        self.cost = float(cost)
        self.team = team.upper() if team else team
        self.matchup = matchup
        self.proj = proj
        self.average_score = average_score
        self.projected_ownership_pct = projected_ownership_pct
        self.lineup_count = lineup_count
        self.marked = marked
        self.lock = lock
        self.position_lock = position_lock
        self.ban = ban
        self.position_ban = False
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

    def to_exposure_table_row(self, n, s_min, s_max):
        return [
            self.formatted_position,
            self.name,
            self.team,
            self.matchup,
            cs(self.cost),
            self.proj,
            n,
            s_min,
            s_max
        ]

    def is_opposing_team_in_match_up(self, team):
        return (team.upper() != self.team.upper()) and \
               (team.upper() in self.matchup.upper())

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

    def __hash__(self):
        return hash((self.pos, self.name, self.cost, self.team))

    def __lt__(self, player):
        if self.cost == player.cost:
            return self.name < player.name
        return self.cost < player.cost

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

    @property
    def short_name(self):
        s = self.name.split()

        # DST
        if len(s) == 1:
            return self.name

        # like "AJ McCarron"
        if re.match(r'^[A-Z]{2}$', s[0]):
            return s

        return '{}. {}'.format(s[0][0], s[1])

    def __set_from_data_cache(self, player_data):
        if player_data is None:
            return
        for k, v in list(player_data.items()):
            setattr(self, k, v)

    def __format_v_avg(self):
        if self.v_avg > 0:
            return '\x1b[0;32;40m{:0.2f}\x1b[0m'.format(self.v_avg)
        return '\x1b[0;31;40m{:0.2f}\x1b[0m'.format(self.v_avg)


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
