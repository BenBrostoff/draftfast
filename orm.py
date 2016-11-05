import numpy as np
import NFL_Draftkings as NFLDK
from constants import ALL_POS_TEAM


class Roster:
    def __init__(self):
        self.players = []

    def __repr__(self):
        s = '\n'.join(str(x) for x in self.sorted_players())
        s += "\n\nProjected Score: %s" % self.projected()
        s += "\tCost: $%s" % self.spent()
        return s

    def __eq__(self, roster):
        if self.__class__ == roster.__class__ and \
           len(self.players) == 9 and len(roster.players) == 9:
            for p in self.players:
                if not any(filter(lambda x: x == p, roster.players)):
                    return False
            return True
        return False

    def add_player(self, player):
        self.players.append(player)

    def spent(self):
        return sum(map(lambda x: x.cost, self.players))

    def projected(self):
        return sum(map(lambda x: x.proj, self.players))

    def position_order(self, player):
        return self.POSITION_ORDER[player.pos]

    def sorted_players(self):
        return sorted(self.players, key=self.position_order)


class NFLRoster(Roster):
    POSITION_ORDER = {
        "QB": 0,
        "RB": 1,
        "WR": 2,
        "TE": 3,
        "DST": 4
    }


class NBARoster(Roster):
    POSITION_ORDER = {
        "PG": 0,
        "SG": 1,
        "SF": 2,
        "PF": 3,
        "C": 4
    }


class RosterSelect:
    @staticmethod
    def roster_gen(league):
        roster_dict = {
            'NBA': NBARoster(),
            'NFL': NFLRoster()
        }
        return roster_dict[league]


class Player:
    _PLAYER_DATA_CACHE = {}

    def __init__(self, pos, name, cost,
                 proj=0, projected_ownership_pct=0,
                 lineup_count=0,
                 matchup=None, team=None,  marked=None,
                 lock=False):
        self.pos = pos
        self.name = name
        self.cost = int(cost)
        self.team = team
        self.matchup = matchup
        self.proj = proj
        self.projected_ownership_pct = projected_ownership_pct
        self.lineup_count = lineup_count
        self.marked = marked
        self.lock = lock

    def __repr__(self):
        return "[{0: <2}] {1: <20} {2} {3} (${4}, {5}, {6}), {7}, {8}".format(
                self.pos,
                self.name,
                self.team,
                self.matchup,
                self.cost,
                self.proj,
                self.get_ppd(),
                self.projected_ownership_pct,
                'LOCK' if self.lock else '')

    def __eq__(self, player):
        return self.pos == player.pos and \
               self.name == player.name and \
               self.cost == player.cost and \
               self.team == player.team

    def get_ppd(self):
        return round((self.proj / self.cost) * 1000, 3)

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
        except:
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


class Team:
    def __init__(self, give):
        self._set_team_pos(give)
        self.team_cost = self._get_team_prop('cost')
        self.team_proj = self._get_team_prop('proj')

    def team_report(self):
        for pos in ALL_POS_TEAM:
            getattr(self, pos).player_report()

        print 'Total Cost: ' + str(self.team_cost)
        print 'Total Projected: ' + str(self.team_proj)

    def contains_dups(self):
        players = []
        for pos in ALL_POS_TEAM:
            name = getattr(self, pos).name
            players.append(name)

        return len(players) != len(set(players))

    def _set_team_pos(self, give):
        for idx, val in enumerate(give):
            setattr(self, ALL_POS_TEAM[idx], val)

    def _get_team_prop(self, prop):
        val = 0
        for pos in ALL_POS_TEAM:
            val += int(getattr(getattr(self, pos), prop))

        return val


class Game:
    def __init__(self, team, opp):
        self.team = team
        self.opponent = opp

    def __repr__(self):
        return "{} @ {}".format(self.team, self.opponent)

    def team_in_game(self, team):
        return team == self.team or team == self.opponent

    def get_teams(self):
        return self.team, self.opponent
