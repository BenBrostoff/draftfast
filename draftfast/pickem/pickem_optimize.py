from draftfast.player_pool import add_pickem_contraints
from draftfast.pickem.pickem_orm import TieredLineup, TIERS
from draftfast.settings import PlayerPoolSettings
from draftfast.lineup_constraints import LineupConstraints
from draftfast.pickem.pickem_orm import TieredPlayer


def optimize(
    all_players: list,
    player_settings: PlayerPoolSettings = PlayerPoolSettings(),
    constraints: LineupConstraints = LineupConstraints()
):
    lineup_players = []
    all_players = list(filter(
        add_pickem_contraints(player_settings),
        all_players
    ))

    if constraints.has_group_constraints():
        raise NotImplementedError('Groups are not supported for pickem')

    for p in all_players:
        if constraints.is_banned(p.name):
            p.ban = True

    for t in TIERS:
        best = sorted(
            [p for p in all_players if p.tier == t and not p.ban],
            key=lambda p: p.proj,
            reverse=True,
        )[0]

        lineup_players.append(best)

    lineup = TieredLineup(lineup_players)

    for p in all_players:
        if constraints.is_locked(p.name):
            p.lock = True
            setattr(lineup, p.tier, p)

    return lineup


def _get_player(name, all_players) -> TieredPlayer:
    return next(
        p for p in all_players if p.name == name
    )
