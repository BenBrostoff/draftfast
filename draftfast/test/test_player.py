
import unittest
assertions = unittest.TestCase('__init__')

from draftfast.orm import Player


def test_player_value():
    pg = Player(name='A', cost=5500, proj=55, pos='PG')
    assertions.assertEquals(pg.value, 10)
