from random import uniform as runiform
from typing import List
from draftfast.orm import Player
from draftfast.settings import PlayerPoolSettings


def filter_pool(pool: list,
                player_settings: PlayerPoolSettings) -> List[Player]:
    if player_settings.randomize:
        for player in pool:
            factor = 1 + runiform(
                -player_settings.randomize,
                player_settings.randomize
            )
            player.proj = player.proj * factor

    return list(filter(
        add_filters(player_settings),
        pool,
    ))


def add_filters(settings: PlayerPoolSettings):
    def filter_fn(player: Player):
        kwargs = {'player': player, 'settings': settings}
        return _is_above_min_cost(**kwargs) and \
            _is_below_max_cost(**kwargs) and \
            _is_above_min_proj(**kwargs) and \
            _is_below_max_proj(**kwargs) and \
            _is_above_min_avg(**kwargs) and \
            _is_below_max_avg(**kwargs)

    return filter_fn


def add_pickem_contraints(settings: PlayerPoolSettings):
    def filter_fn(player: Player):
        # TODO - add team banning
        kwargs = {'player': player, 'settings': settings}
        return (
            _is_above_min_proj(**kwargs) and
            # (not _is_banned_team(**kwargs)) and
            # _is_locked_team(**kwargs) and
            # _is_within_avg(**kwargs) and
            _is_above_min_avg(**kwargs)
        )

    return filter_fn


def lock_override(fn):
    def override_fn(**kwargs):
        if kwargs['player'].lock:
            return True
        return fn(**kwargs)

    return override_fn


@lock_override
def _is_above_min_cost(player, settings):
    if settings.min_salary is None:
        return True
    return player.cost >= settings.min_salary


@lock_override
def _is_below_max_cost(player, settings):
    if settings.max_salary is None:
        return True
    return player.cost <= settings.max_salary


@lock_override
def _is_above_min_proj(player, settings):
    if settings.min_proj is None:
        return True
    return player.proj >= settings.min_proj


@lock_override
def _is_below_max_proj(player, settings):
    if settings.max_proj is None:
        return True
    return player.proj <= settings.max_proj


@lock_override
def _is_above_min_avg(player, settings):
    if settings.min_avg is None:
        return True
    return player.average_score >= settings.min_avg


@lock_override
def _is_below_max_avg(player, settings):
    if settings.max_avg is None:
        return True
    return player.average_score <= settings.max_avg
