from draftfast.player_pool import add_pickem_contraints
from draftfast.pickem.pickem_orm import TieredLineup, TIERS
from draftfast.settings import PickemSettings, PlayerPoolSettings


def optimize(all_players, player_settings=PlayerPoolSettings(),
             pickem_settings=PickemSettings()):
    lineup_players = []
    all_players = list(filter(
        add_pickem_contraints(player_settings),
        all_players
    ))
    for t in TIERS:
        best = sorted(
            [p for p in all_players if p.tier == t],
            key=lambda p: p.proj,
            reverse=True,
        )[0]

        lineup_players.append(best)

    lineup = TieredLineup(lineup_players)
    locked = pickem_settings.locked
    if locked:
        for lock in locked:
            player_lock = _get_player(lock, all_players)
            player_lock.locked = True
            setattr(
                lineup,
                player_lock.tier,
                player_lock,
            )

    return lineup


def _get_player(name, all_players):
    return next(
        p for p in all_players if p.name == name
    )
