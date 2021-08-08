from draftfast.orm import NFLRoster, Player, ShowdownRoster
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

    ntool.assert_false(roster_a == roster_c)
    ntool.assert_true(roster_a == roster_b)


def test_roster_equality_with_position_shuffle():
    player_a = Player(pos='RB', name='A', cost=1, team='X')
    player_a_new_pos = Player(pos='WR', name='A', cost=1, team='X')
    player_b = Player(pos='QB', name='B', cost=1, team='X')
    player_c = Player(pos='QB', name='C', cost=1, team='X')

    roster_a = NFLRoster()
    roster_a.add_player(player_a)
    roster_a.add_player(player_b)

    roster_b = NFLRoster()
    roster_b.add_player(player_a_new_pos)
    roster_b.add_player(player_b)

    roster_c = NFLRoster()
    roster_c.add_player(player_a)
    roster_c.add_player(player_c)

    ntool.assert_false(roster_a == roster_c)
    ntool.assert_true(roster_a == roster_b)


def test_showdown_roster_equality_and_position_shuffle():
    """
    In Showdown, point changes result from CPT assignment,
    so two lineups are not equal given the same player.
    """
    player_a = Player(pos='FLEX', name='A', cost=1, team='A')
    player_a_new_pos = Player(pos='CPT', name='A', cost=1, team='A')
    player_b = Player(pos='FLEX', name='B', cost=1, team='C')
    player_c = Player(pos='FLEX', name='C', cost=1, team='D')

    roster_a = ShowdownRoster()
    roster_a.add_player(player_a)
    roster_a.add_player(player_b)

    roster_b = ShowdownRoster()
    roster_b.add_player(player_a_new_pos)
    roster_b.add_player(player_b)

    roster_c = ShowdownRoster()
    roster_c.add_player(player_a)
    roster_c.add_player(player_c)

    ntool.assert_false(roster_a == roster_c)
    ntool.assert_false(roster_a == roster_b)


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
