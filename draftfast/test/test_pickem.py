import unittest
from draftfast.pickem import pickem_orm
from draftfast.pickem.pickem_optimize import optimize
from draftfast.settings import PlayerPoolSettings
from draftfast.lineup_constraints import LineupConstraints

assertions = unittest.TestCase("__init__")


def _generate_player(name, proj, tier, **kwargs):
    return pickem_orm.TieredPlayer(
        cost=0,
        name=name,
        proj=proj,
        tier=tier,
        pos=kwargs.get("pos"),
        team=kwargs.get("team"),
        matchup=kwargs.get("matchup"),
        average_score=kwargs.get("average_score", 0),
    )


_BOS = "BOS"
_GS = "GS"


def _generate_test_player_data():
    return [
        _generate_player("A", 50, pickem_orm.T1, team=_BOS),
        _generate_player("B", 49, pickem_orm.T1, team=_GS),
        _generate_player("C", 48, pickem_orm.T2, team=_BOS),
        _generate_player("D", 47, pickem_orm.T2, team=_GS),
        _generate_player("E", 46, pickem_orm.T3, team=_BOS),
        _generate_player("F", 45, pickem_orm.T3, team=_GS),
        _generate_player("G", 44, pickem_orm.T4, team=_BOS),
        _generate_player("H", 43, pickem_orm.T4, team=_GS),
        _generate_player("I", 42, pickem_orm.T5, team=_BOS),
        _generate_player("J", 41, pickem_orm.T5, team=_GS),
        _generate_player("K", 40, pickem_orm.T6, team=_BOS),
        _generate_player("L", 39, pickem_orm.T6, team=_GS),
    ]


def test_default_lineup():
    players = _generate_test_player_data()
    optimized = optimize(players)
    assertions.assertEqual(optimized.total, 50 + 48 + 46 + 44 + 42 + 40)


def test_banned_players():
    players = _generate_test_player_data()

    optimized = optimize(
        players,
        player_settings=PlayerPoolSettings(),
        constraints=LineupConstraints(banned=["A", "C"]),
    )
    assertions.assertEqual(optimized.total, 49 + 47 + 46 + 44 + 42 + 40)


def test_locked_players():
    players = _generate_test_player_data()

    optimized = optimize(
        players, constraints=LineupConstraints(locked=["B", "D"])
    )
    assertions.assertEqual(optimized.total, 49 + 47 + 46 + 44 + 42 + 40)


#
#
# def test_banned_teams():
#     players = _generate_test_player_data()
#     test_args = args_dict.copy()
#     test_args['banned_teams'] = [_BOS]
#     optimized = optimize(players, cmd_args=Namespace(**test_args))
#     assertions.assertEqual(
#         optimized.total,
#         49 + 47 + 45 + 43 + 41 + 39
#     )
#
#
# def test_locked_teams():
#     players = _generate_test_player_data()
#     test_args = args_dict.copy()
#     test_args['locked_teams'] = [_GS]
#     optimized = optimize(players, cmd_args=Namespace(**test_args))
#     assertions.assertEqual(
#         optimized.total,
#         49 + 47 + 45 + 43 + 41 + 39
#     )
