from nose import tools as ntools
from draftfast.optimize import run
from draftfast import rules
from draftfast.orm import Player
from draftfast.settings import OptimizerSettings
from draftfast.showdown.orm import ShowdownPlayer


def _build_mock_player_pool():
    player_pool = [
        Player(name='A1', cost=5500, proj=100, pos='QB',
               team='X', matchup='X@Y'),
        Player(name='A2', cost=5500, proj=41, pos='QB',
               team='X', matchup='X@Y'),
        Player(name='A11', cost=5500, proj=50, pos='WR',
               team='X', matchup='X@Y'),
        Player(name='A3', cost=5500, proj=42, pos='WR',
               team='X', matchup='X@Y'),
        Player(name='A4', cost=5500, proj=43, pos='WR',
               team='X', matchup='X@Y'),
        Player(name='A5', cost=5500, proj=44, pos='WR',
               team='X', matchup='X@Y'),
        Player(name='A6', cost=5500, proj=45, pos='RB',
               team='X', matchup='X@Y'),

        # Test that max players per team works. Everyone
        # on Y is projected for 1 point, under normal
        # opto should never be picked.
        Player(name='A7', cost=5500, proj=1, pos='RB',
               team='Y', matchup='X@Y'),
        Player(name='A8', cost=5500, proj=1, pos='RB',
               team='Y', matchup='X@Y'),
        Player(name='A9', cost=5500, proj=1, pos='TE',
               team='Y', matchup='X@Y'),
    ]

    def capt_boost(p):
        return Player(
            name=p.name,
            team=p.team,
            matchup=p.matchup,
            pos=p.pos,
            cost=p.cost * 1.5,
            proj=p.proj * 1.5,
        )

    captain_pool = [capt_boost(p) for p in player_pool]

    mock_dk_pool = []
    for p in player_pool:
        mock_dk_pool.append(ShowdownPlayer(p))
    for p in captain_pool:
        mock_dk_pool.append(ShowdownPlayer(p, captain=True))

    return mock_dk_pool


def test_csgo_mock():
    mock_dk_pool = _build_mock_player_pool()

    roster = run(
        # CSGO limits three per team
        rule_set=rules.DK_CSGO_SHOWDOWN,
        player_pool=mock_dk_pool,
        optimizer_settings=OptimizerSettings(
            showdown_teams=('X', 'Y'),
        ),
        verbose=True
    )

    ntools.assert_not_equal(roster, None)
    players = roster.players
    ntools.assert_equal(len([
        x for x in players if x.team == 'Y'
    ]), 3)
