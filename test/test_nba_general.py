from orm import Player


def test_general_guard():
    pg = Player(name='A', cost=1, proj=1, pos='PG')
    assert pg.nba_general_position == 'G'
    sg = Player(name='A', cost=1, proj=1, pos='SG')
    assert sg.nba_general_position == 'G'


def test_general_forward():
    pg = Player(name='A', cost=1, proj=1, pos='SF')
    assert pg.nba_general_position == 'F'
    sg = Player(name='A', cost=1, proj=1, pos='PF')
    assert sg.nba_general_position == 'F'


def test_general_center():
    pg = Player(name='A', cost=1, proj=1, pos='C')
    assert pg.nba_general_position == 'C'
