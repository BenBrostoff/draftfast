from draftfast.orm import NFLRoster, Player
from nose import tools as ntool


def test_roster_equality():
    player_a = Player(pos='RB', name='A', cost=1, team='X')
    player_b = Player(pos='QB', name='B', cost=1, team='X')
    player_c = Player(pos='QB', name='C', cost=1, team='X')

    roster_a = NFLRoster()
    roster_a.add_player(player_a)
    roster_a.add_player(player_b)

    roster_b = NFLRoster()
    roster_b.add_player(player_a)
    roster_b.add_player(player_b)

    roster_c = NFLRoster()
    roster_c.add_player(player_a)
    roster_c.add_player(player_c)

    ntool.assert_false(roster_a.exact_equal(roster_c))
    ntool.assert_false(roster_a == roster_c)
    ntool.assert_true(roster_a.exact_equal(roster_b))
    ntool.assert_true(roster_a == roster_b)


def test_roster_set():
    player_a = Player(pos='RB', name='A', cost=1, team='X')
    player_b = Player(pos='QB', name='B', cost=1, team='X')
    player_c = Player(pos='QB', name='C', cost=1, team='X')

    roster_a = NFLRoster()
    roster_a.add_player(player_a)
    roster_a.add_player(player_b)

    roster_b = NFLRoster()
    roster_b.add_player(player_a)
    roster_b.add_player(player_b)

    roster_c = NFLRoster()
    roster_c.add_player(player_a)
    roster_c.add_player(player_c)
    ntool.assert_true(len(set([roster_a, roster_b, roster_c])), 2)
