import unittest
from draftfast.orm import Player

assertions = unittest.TestCase('__init__')


def test_player_value():
    pg = Player(name='A', cost=5500, proj=55, pos='PG')
    assertions.assertEquals(pg.value, 10)
