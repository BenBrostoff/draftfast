import random
from nose import tools as ntools
from draftfast.player_pool import filter_pool
from draftfast.orm import Player
from draftfast.settings import PlayerPoolSettings


p_a, p_b, p_c = [
    Player(name='A1', cost=5500, proj=20, pos='PG'),
    Player(name='A2', cost=7000, proj=30, pos='PG'),
    Player(name='A3', cost=10000, proj=55, pos='PG'),
]
mock_player_pool = [p_a, p_b, p_c]


def test_no_settings():
    pool = filter_pool(mock_player_pool, PlayerPoolSettings())
    ntools.assert_equals(pool, mock_player_pool)


def test_respects_min_proj():
    pool = filter_pool(mock_player_pool, PlayerPoolSettings(min_proj=50))
    ntools.assert_equals(pool, [p_c])


def test_respects_max_proj():
    pool = filter_pool(mock_player_pool, PlayerPoolSettings(max_proj=50))
    ntools.assert_equals(pool, [p_a, p_b])


def test_respects_min_cost():
    pool = filter_pool(mock_player_pool, PlayerPoolSettings(min_salary=7001))
    ntools.assert_equals(pool, [p_c])


def test_respects_max_cost():
    pool = filter_pool(mock_player_pool, PlayerPoolSettings(max_salary=7001))
    ntools.assert_equals(pool, [p_a, p_b])


def test_randomize():
    random.seed(1)
    pool = filter_pool(mock_player_pool, PlayerPoolSettings(
        randomize=0.1,
    ))
    ntools.assert_equals(
        pool[0].proj,
        18.537456976449604
    )
