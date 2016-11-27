import numpy as np
import NFL_Draftkings as NFLDK


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
        try:
            return self.POSITION_ORDER[player.pos]
        except KeyError:
            # Hack to deal with multi-position players
            # See outstanding GitHub issue
            first_pos = player.pos.split('/')[0]
            return self.POSITION_ORDER[first_pos]

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
                 average_score=0,
                 matchup=None, team=None,  marked=None,
                 lock=False):
        self.pos = pos
        self.name = name
        self.cost = int(cost)
        self.team = team
        self.matchup = matchup
        self.proj = proj
        self.average_score = average_score
        self.projected_ownership_pct = projected_ownership_pct
        self.lineup_count = lineup_count
        self.marked = marked
        self.lock = lock

    def __repr__(self):
        player_dict = dict(
            pos=self.pos,
            name=self.name,
            team=self.team,
            match=self.matchup,
            cost=self.cost,
            proj=self.proj,
            diff=self.proj - self.average_score,
            lock='LOCK' if self.lock else ''
        )

        return "[{pos: <2}] {name: <20} {team} {match} " \
               "(${cost}, {proj} ({diff})), {lock}".format(
                **player_dict)

    def __eq__(self, player):
        return self.pos == player.pos and \
               self.name == player.name and \
               self.cost == player.cost and \
               self.team == player.team

    @property
    def is_home(self):
        match_up_teams = self.matchup.split(' ')[0]
        return self.team == match_up_teams.split('@')[-1]

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
