from draftfast.orm import (
    NFLRoster,
    Player,
    ShowdownRoster,
    RosterGroup,
    MVPRoster,
)
import unittest

assertions = unittest.TestCase("__init__")


def test_roster_equality():
    player_a = Player(pos="RB", name="A", cost=1, team="X")
    player_b = Player(pos="QB", name="B", cost=1, team="X")
    player_c = Player(pos="QB", name="C", cost=1, team="X")

    roster_a = NFLRoster()
    roster_a.add_player(player_a)
    roster_a.add_player(player_b)

    roster_b = NFLRoster()
    roster_b.add_player(player_a)
    roster_b.add_player(player_b)

    roster_c = NFLRoster()
    roster_c.add_player(player_a)
    roster_c.add_player(player_c)

    assertions.assertFalse(roster_a == roster_c)
    assertions.assertTrue(roster_a == roster_b)


def test_roster_equality_with_position_shuffle():
    player_a = Player(pos="RB", name="A", cost=1, team="X")
    player_a_new_pos = Player(pos="WR", name="A", cost=1, team="X")
    player_b = Player(pos="QB", name="B", cost=1, team="X")
    player_c = Player(pos="QB", name="C", cost=1, team="X")

    roster_a = NFLRoster()
    roster_a.add_player(player_a)
    roster_a.add_player(player_b)

    roster_b = NFLRoster()
    roster_b.add_player(player_a_new_pos)
    roster_b.add_player(player_b)

    roster_c = NFLRoster()
    roster_c.add_player(player_a)
    roster_c.add_player(player_c)

    assertions.assertFalse(roster_a == roster_c)
    assertions.assertTrue(roster_a == roster_b)


def test_showdown_roster_equality_and_position_shuffle():
    """
    In Showdown, point changes result from CPT assignment,
    so two lineups are not equal given the same player.
    """
    player_a = Player(pos="UTIL", name="A", cost=1, team="A")
    player_a_new_pos = Player(pos="MVP", name="A", cost=1, team="A")
    player_b = Player(pos="UTIL", name="B", cost=1, team="C")
    player_c = Player(pos="UTIL", name="C", cost=1, team="D")

    roster_a = MVPRoster()
    roster_a.add_player(player_a)
    roster_a.add_player(player_b)

    roster_b = MVPRoster()
    roster_b.add_player(player_a_new_pos)
    roster_b.add_player(player_b)

    roster_c = MVPRoster()
    roster_c.add_player(player_a)
    roster_c.add_player(player_c)

    assertions.assertFalse(roster_a == roster_c)
    assertions.assertFalse(roster_a == roster_b)


def test_mvp_roster_equality_and_position_shuffle():
    """
    In Showdown, point changes result from CPT assignment,
    so two lineups are not equal given the same player.
    """
    player_a = Player(pos="FLEX", name="A", cost=1, team="A")
    player_a_new_pos = Player(pos="CPT", name="A", cost=1, team="A")
    player_b = Player(pos="FLEX", name="B", cost=1, team="C")
    player_c = Player(pos="FLEX", name="C", cost=1, team="D")

    roster_a = ShowdownRoster()
    roster_a.add_player(player_a)
    roster_a.add_player(player_b)

    roster_b = ShowdownRoster()
    roster_b.add_player(player_a_new_pos)
    roster_b.add_player(player_b)

    roster_c = ShowdownRoster()
    roster_c.add_player(player_a)
    roster_c.add_player(player_c)

    assertions.assertFalse(roster_a == roster_c)
    assertions.assertFalse(roster_a == roster_b)


def test_roster_set():
    player_a = Player(pos="RB", name="A", cost=1, team="X")
    player_b = Player(pos="QB", name="B", cost=1, team="X")
    player_c = Player(pos="QB", name="C", cost=1, team="X")

    roster_a = NFLRoster()
    roster_a.add_player(player_a)
    roster_a.add_player(player_b)

    roster_b = NFLRoster()
    roster_b.add_player(player_a)
    roster_b.add_player(player_b)

    roster_c = NFLRoster()
    roster_c.add_player(player_a)
    roster_c.add_player(player_c)
    assertions.assertTrue(len(set([roster_a, roster_b, roster_c])), 2)


def test_roster_group():
    player_a = Player(pos="RB", name="A", cost=1, team="X")
    player_b = Player(pos="QB", name="B", cost=1, team="X")
    player_c = Player(pos="QB", name="C", cost=1, team="X")

    roster_a = NFLRoster()
    roster_a.add_player(player_a)
    roster_a.add_player(player_b)

    roster_b = NFLRoster()
    roster_b.add_player(player_a)
    roster_b.add_player(player_b)

    roster_c = NFLRoster()
    roster_c.add_player(player_a)
    roster_c.add_player(player_c)

    rg = RosterGroup(rosters=[roster_a, roster_b])
    assertions.assertEqual(rg.get_similarity_score(), 1)
    assertions.assertEqual(rg.get_salary_frequency(), [(2, 2)])
    assertions.assertEqual(
        rg.get_player_frequency(), [(player_a, 2), (player_b, 2)]
    )

    rg_2 = RosterGroup(rosters=[roster_a, roster_c])
    assertions.assertEqual(rg_2.get_similarity_score(), 0.5)

    rg_3 = RosterGroup(rosters=[roster_a, roster_b, roster_c])
    assertions.assertEqual(
        rg_3.get_similarity_score(),
        # (1 + 0.5 + 0.5)/3
        2 / 3,
    )

    roster_d = NFLRoster()
    roster_d.add_player(player_a)
    roster_d.add_player(Player(pos="QB", name="D", cost=1, team="X"))

    # All lineups share half of the same players
    rg_4 = RosterGroup(rosters=[roster_a, roster_c, roster_d])
    assertions.assertEqual(
        rg_4.get_similarity_score(),
        # (0.5 + 0.5 + 0.5)/3
        0.5,
    )


def test_shared_and_different_player_count():
    player_a = Player(pos="RB", name="A", cost=1, team="X")
    player_b = Player(pos="QB", name="B", cost=1, team="X")
    player_c = Player(pos="QB", name="C", cost=1, team="X")

    roster_a = NFLRoster()
    roster_a.add_player(player_a)
    roster_a.add_player(player_b)

    roster_b = NFLRoster()
    roster_b.add_player(player_a)
    roster_b.add_player(player_b)

    roster_c = NFLRoster()
    roster_c.add_player(player_a)
    roster_c.add_player(player_c)

    assertions.assertEqual(roster_a.different_player_count(roster_b), 0)
    assertions.assertEqual(roster_a.shared_player_count(roster_b), 2)
    assertions.assertEqual(roster_a.different_player_count(roster_c), 1)
    assertions.assertEqual(roster_a.shared_player_count(roster_c), 1)
    assertions.assertEqual(roster_b.different_player_count(roster_c), 1)
    assertions.assertEqual(roster_b.shared_player_count(roster_c), 1)
