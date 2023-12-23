from draftfast.lineup_constraints import (
    LineupConstraints,
    ConstraintConflictException,
    ConstraintException,
)

import unittest

assertions = unittest.TestCase("__init__")


def test_constraint_string_args():
    lcs = LineupConstraints()
    lcs.ban("Sam Bradford")
    lcs.lock("Will Fuller")
    assertions.assertEqual(len(lcs), 2)


def test_constraint_contains():
    lcs = LineupConstraints()
    lcs.add_group_constraint(["A", "B"], 1)
    lcs.ban(["C"])
    lcs.add_group_constraint(["E", "F", "G"], (1, 3))
    lcs.lock(["H"])

    for c in ["A", "B", "C", "E", "F", "G", "H"]:
        assertions.assertEqual(c in lcs, True)


def test_constraint_set_eq():
    lcs1 = LineupConstraints()
    lcs1.add_group_constraint(["Spencer Ware", "Amari Cooper"], 1)
    lcs1.ban(["Packers"])
    lcs1.add_group_constraint(
        ["Eli Manning", "Russell Wilson", "Doug Martin"], (1, 3)
    )
    lcs1.lock(["Will Fuller"])

    lcs2 = LineupConstraints()
    lcs2.add_group_constraint(["Spencer Ware", "Amari Cooper"], 1)
    lcs2.ban(["Packers"])
    lcs2.add_group_constraint(
        ["Eli Manning", "Russell Wilson", "Doug Martin"], (1, 3)
    )
    lcs2.lock(["Will Fuller"])

    assertions.assertEqual(lcs1, lcs2)


def test_build_constraint_set():
    lcs = LineupConstraints()
    lcs.add_group_constraint(["Spencer Ware", "Amari Cooper"], 1)
    lcs.ban(["Packers"])
    lcs.add_group_constraint(
        ["Eli Manning", "Russell Wilson", "Doug Martin"], (1, 3)
    )
    lcs.lock(["Will Fuller"])

    assertions.assertEqual(len(lcs), 4)


def test_dup_group_rule():
    with assertions.assertRaises(ConstraintConflictException):
        lcs = LineupConstraints()
        lcs.add_group_constraint(["Spencer Ware", "Amari Cooper"], 1)
        lcs.add_group_constraint(["Spencer Ware", "Amari Cooper"], 1)


def test_dup_group_rule2():
    with assertions.assertRaises(ConstraintConflictException):
        lcs = LineupConstraints()
        lcs.add_group_constraint(
            ["Eli Manning", "Russell Wilson", "Doug Martin"], (1, 2)
        )
        lcs.add_group_constraint(
            ["Eli Manning", "Russell Wilson", "Doug Martin"], (1, 2)
        )


def test_bad_group_shadow_lock_bound():
    with assertions.assertRaises(ConstraintException):
        lcs = LineupConstraints()
        lcs.add_group_constraint(["Spencer Ware", "Amari Cooper"], 2)


def test_bad_group_shadow_lock_hi_lo_bound():
    with assertions.assertRaises(ConstraintException):
        lcs = LineupConstraints()
        lcs.add_group_constraint(["Spencer Ware", "Amari Cooper"], (2, 2))


def test_bad_group_shadow_ban_bound():
    with assertions.assertRaises(ConstraintException):
        lcs = LineupConstraints()
        lcs.add_group_constraint(["Spencer Ware", "Amari Cooper"], 0)


def test_bad_group_shadow_ban_hi_lo_bound():
    with assertions.assertRaises(ConstraintException):
        lcs = LineupConstraints()
        lcs.add_group_constraint(["Spencer Ware", "Amari Cooper"], (0, 0))


def test_bad_group_duplicate_bounds():
    with assertions.assertRaises(ConstraintException):
        lcs = LineupConstraints()
        lcs.add_group_constraint(["Spencer Ware", "Amari Cooper"], (1, 1))


def test_bad_group_negative_min():
    with assertions.assertRaises(ConstraintException):
        lcs = LineupConstraints()
        lcs.add_group_constraint(["Spencer Ware", "Amari Cooper"], (-1, 1))


def test_bad_group_zero_min():
    with assertions.assertRaises(ConstraintException):
        lcs = LineupConstraints()
        lcs.add_group_constraint(["Spencer Ware", "Amari Cooper"], (0, 1))


def test_bad_group_max():
    with assertions.assertRaises(ConstraintException):
        lcs = LineupConstraints()
        lcs.add_group_constraint(["Spencer Ware", "Amari Cooper"], 3)


def test_bad_group_max_set():
    with assertions.assertRaises(ConstraintException):
        lcs = LineupConstraints()
        lcs.add_group_constraint(["Spencer Ware", "Amari Cooper"], (1, 3))


def test_bad_group_dup_player():
    with assertions.assertRaises(ConstraintException):
        lcs = LineupConstraints()
        lcs.add_group_constraint(["Amari Cooper", "Amari Cooper"], 1)


def test_bad_group_bounds_type():
    with assertions.assertRaises(ConstraintException):
        lcs = LineupConstraints()
        lcs.add_group_constraint(["Spencer Ware", "Amari Cooper"], "1")


def test_bad_group_too_many_bounds():
    with assertions.assertRaises(ConstraintException):
        lcs = LineupConstraints()
        lcs.add_group_constraint(["Spencer Ware", "Amari Cooper"], (1, 1, 2))


def test_single_player_group():
    with assertions.assertRaises(ConstraintException):
        lcs = LineupConstraints()
        lcs.add_group_constraint(["Spencer Ware"], 1)


def test_empty_group():
    with assertions.assertRaises(ConstraintException):
        lcs = LineupConstraints()
        lcs.add_group_constraint([], 1)


def test_empty_lock():
    with assertions.assertRaises(ConstraintException):
        lcs = LineupConstraints()
        lcs.lock([])


def test_empty_ban():
    with assertions.assertRaises(ConstraintException):
        lcs = LineupConstraints()
        lcs.ban([])


def test_ban_lock_conflict():
    with assertions.assertRaises(ConstraintConflictException):
        lcs = LineupConstraints()
        lcs.lock(["Will Fuller"])
        lcs.ban(["Will Fuller"])


def test_lock_ban_conflict():
    with assertions.assertRaises(ConstraintConflictException):
        lcs = LineupConstraints()
        lcs.ban(["Will Fuller"])
        lcs.lock(["Will Fuller"])


def test_lock_group_conflict():
    with assertions.assertRaises(ConstraintConflictException):
        lcs = LineupConstraints()
        lcs.lock(["Eli Manning"])
        lcs.add_group_constraint(["Eli Manning", "Doug Martin"], (1, 2))


def test_group_lock_conflict():
    with assertions.assertRaises(ConstraintConflictException):
        lcs = LineupConstraints()
        lcs.add_group_constraint(["Eli Manning", "Doug Martin"], (1, 2))
        lcs.lock(["Eli Manning"])


def test_ban_group_conflict():
    with assertions.assertRaises(ConstraintConflictException):
        lcs = LineupConstraints()
        lcs.ban(["Eli Manning"])
        lcs.add_group_constraint(["Eli Manning", "Doug Martin"], (1, 2))


def test_group_ban_conflict():
    with assertions.assertRaises(ConstraintConflictException):
        lcs = LineupConstraints()
        lcs.add_group_constraint(["Eli Manning", "Doug Martin"], (1, 2))
        lcs.ban(["Eli Manning"])
