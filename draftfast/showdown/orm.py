from draftfast.orm import Player
from typing import Optional
from copy import deepcopy


class ShowdownPlayer(Player):

    # Captain and MVP multiplier
    # TODO - make public
    _CAPTAIN_MULTIPLIER = 1.5

    def __init__(
        self,
        player: Player,
        captain: bool = False,
        pos: Optional[str] = None
    ):
        for k, v in player.__dict__.items():
            if hasattr(self, k) or k.startswith('__'):
                continue
            setattr(self, k, deepcopy(v))

        if captain:
            self.real_pos = self.pos
            self.pos = 'CPT'
            self.captain = True
        else:
            if pos:
                self.pos = pos
                self.real_pos = pos
            else:
                self.real_pos = self.pos
                self.pos = 'FLEX'

            self.captain = False

    @property
    def formatted_position(self):
        return '{} ({})'.format(self.pos, self.real_pos)

    @property
    def is_captain(self):
        return self.pos == 'CPT'

    @property
    def roster_id(self):
        """
        Used for roster equality.
        Unlike classic, position matters in showdown at CPT level.
        """
        return f'{self.name} {self.team} {self.is_captain}'

    @property
    def v_avg(self):
        """
        Normalize average comparison for captain.
        """
        if self.is_captain:
            return self.proj / self._CAPTAIN_MULTIPLIER - self.average_score
        return self.proj - self.average_score


class MVPPlayer(Player):
    MVP_MULTIPLIER = 2
    STAR_MULTIPLIER = 1.5
    PRO_MULTIPLIER = 1.2

    @classmethod
    def from_player(cls, player, game_position):
        player = cls(
            player.pos,
            name=player.name,
            cost=player.cost,
            proj=player.proj,
            projected_ownership_pct=player.projected_ownership_pct,
            lineup_count=player.lineup_count,
            average_score=player.average_score,
            matchup=player.matchup,
            team=player.team,
            marked=player.marked,
            possible_positions=player.possible_positions,
            lock=player.lock,
            position_lock=player.position_lock,
            ban=player.ban,
            multi_position=player.multi_position,
            kv_store=player.kv_store,
        )
        player.real_pos = player.pos

        # MVP, STAR, PRO, UTIL
        player.pos = game_position

        return player

    @property
    def roster_id(self):
        """
        Used for roster equality.
        Unlike classic, multipliers exist at MVP and star levels
        """
        return f'{self.name} {self.team} {self.pos}'
