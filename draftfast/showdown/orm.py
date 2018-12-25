from draftfast.orm import Player
from terminaltables import AsciiTable
from copy import deepcopy 

class ShowdownPlayer(Player):
    def __init__(self, player: Player, captain: bool=False):
        for k, v in player.__dict__.iteritems():
            if hasattr(self, k) or k.startswith('__'):
                continue
            setattr(self, k, deepcopy(v))

        if captain:
            self.showdown_pos = 'CAPT'
            self.proj *= 1.5
        else:
            self.showdown_pos = 'FLEX'

    @property
    def formatted_position(self):
        return '{} ({})'.format(self.showdown_pos, self.pos)
