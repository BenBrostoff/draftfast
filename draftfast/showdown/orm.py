from draftfast.orm import Player
from terminaltables import AsciiTable


class ShowdownPlayer(Player):
    def set_captain(self):
        self.proj *= 1.5
        self.captain = True

    @property
    def formatted_position(self):
        return '{} ({})'.format('CAPT' if self.captain else 'FLEX', self.pos)
