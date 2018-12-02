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


def test_respects_banned():
    pool = filter_pool(
        mock_player_pool,
        PlayerPoolSettings(banned=['A1', 'A2'])
    )
    ntools.assert_equals(pool, [p_c])


def test_respects_locked():
    pool = filter_pool(mock_player_pool, PlayerPoolSettings(
        locked=['A2'],
        min_proj=31,
    ))
    ntools.assert_equals(pool, [p_b, p_c])
