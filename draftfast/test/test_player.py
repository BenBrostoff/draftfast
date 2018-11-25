from nose import tools as ntools
from draftfast.orm import Player


def test_player_value():
    pg = Player(name='A', cost=5500, proj=55, pos='PG')
    ntools.assert_equal(pg.value, 10)
