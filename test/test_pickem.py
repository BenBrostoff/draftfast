from pickem import pickem_orm
from pickem.pickem_optimize import optimize
from nose import tools as ntools


def _generate_player(name, proj, tier, **kwargs):
    return pickem_orm.TieredPlayer(
        cost=0,
        name=name,
        proj=proj,
        tier=tier,
        pos=kwargs.get('pos'),
        team=kwargs.get('team'),
        matchup=kwargs.get('matchup'),
        average_score=kwargs.get('average_score', 0),
    )


def _generate_test_player_data():
    return [
        _generate_player('A', 50, pickem_orm.TIER_1),
        _generate_player('B', 49, pickem_orm.TIER_1),
        _generate_player('C', 48, pickem_orm.TIER_2),
        _generate_player('D', 47, pickem_orm.TIER_2),
        _generate_player('E', 46, pickem_orm.TIER_3),
        _generate_player('F', 45, pickem_orm.TIER_3),
        _generate_player('G', 44, pickem_orm.TIER_4),
        _generate_player('H', 43, pickem_orm.TIER_4),
        _generate_player('I', 42, pickem_orm.TIER_5),
        _generate_player('J', 41, pickem_orm.TIER_5),
        _generate_player('K', 40, pickem_orm.TIER_6),
        _generate_player('L', 39, pickem_orm.TIER_6),
    ]


def test_default_lineup():
    players = _generate_test_player_data()
    optimized = optimize(players)
    ntools.assert_equal(
        optimized.total,
        50 + 48 + 46 + 44 + 42 + 40
    )
