from draftfast.orm import Player
from terminaltables import AsciiTable
from copy import deepcopy

class ShowdownPlayer(Player):
    def __init__(self, player: Player, captain: bool=False):
        for k, v in player.__dict__.items():
            if hasattr(self, k) or k.startswith('__'):
                continue
            setattr(self, k, deepcopy(v))

        if captain:
            self.real_pos = self.pos
            self.pos = 'CAPT'
            self.captain = True
            self.proj *= 1.5
            self.cost *= 1.5
        else:
            self.real_pos = self.pos
            self.pos = 'FLEX'
            self.captain = False

    @property
    def formatted_position(self):
        return '{} ({})'.format(self.pos, self.real_pos)
