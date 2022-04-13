from draftfast.orm import Player
from typing import Optional
from copy import deepcopy


class ShowdownPlayer(Player):
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
            return self.proj / 1.5 - self.average_score
        return self.proj - self.average_score
