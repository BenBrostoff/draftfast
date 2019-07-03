from draftfast.orm import Player
from copy import deepcopy


class ShowdownPlayer(Player):
    def __init__(self, player: Player, captain: bool = False):
        for k, v in player.__dict__.items():
            if hasattr(self, k) or k.startswith('__'):
                continue
            setattr(self, k, deepcopy(v))

        if captain:
            self.real_pos = self.pos
            self.pos = 'CPT'
            self.captain = True
        else:
            self.real_pos = self.pos
            self.pos = 'FLEX'
            self.captain = False

    @property
    def formatted_position(self):
        return '{} ({})'.format(self.pos, self.real_pos)

    @property
    def v_avg(self):
        if self.pos == 'CPT':
            return self.proj / 1.5 - self.average_score
        return self.proj - self.average_score
