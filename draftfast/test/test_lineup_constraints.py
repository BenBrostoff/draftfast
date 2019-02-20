from draftfast.lineup_constraints import (LineupConstraints,
                                          ConstraintConflictException,
                                          ConstraintException)
from nose import tools as ntools


def test_constraint_string_args():
    lcs = LineupConstraints()
    lcs.ban('Sam Bradford')
    lcs.lock('Will Fuller')
    ntools.assert_equal(len(lcs), 2)


def test_constraint_contains():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['A', 'B'], 1)
    lcs.ban(['C'])
    lcs.add_group_constraint(['E', 'F', 'G'], (1, 3))
    lcs.lock(['H'])

    for c in ['A', 'B', 'C', 'E', 'F', 'G', 'H']:
        ntools.assert_equal(c in lcs, True)


def test_constraint_set_eq():
    lcs1 = LineupConstraints()
    lcs1.add_group_constraint(['Spencer Ware', 'Amari Cooper'], 1)
    lcs1.ban(['Packers'])
    lcs1.add_group_constraint(['Eli Manning', 'Russell Wilson', 'Doug Martin'],
                              (1, 3))
    lcs1.lock(['Will Fuller'])

    lcs2 = LineupConstraints()
    lcs2.add_group_constraint(['Spencer Ware', 'Amari Cooper'], 1)
    lcs2.ban(['Packers'])
    lcs2.add_group_constraint(['Eli Manning', 'Russell Wilson', 'Doug Martin'],
                              (1, 3))
    lcs2.lock(['Will Fuller'])

    ntools.assert_equal(lcs1, lcs2)


def test_build_constraint_set():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Spencer Ware', 'Amari Cooper'], 1)
    lcs.ban(['Packers'])
    lcs.add_group_constraint(['Eli Manning', 'Russell Wilson', 'Doug Martin'],
                             (1, 3))
    lcs.lock(['Will Fuller'])

    ntools.assert_equal(len(lcs), 4)


@ntools.raises(ConstraintConflictException)
def test_dup_group_rule():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Spencer Ware', 'Amari Cooper'], 1)
    lcs.add_group_constraint(['Spencer Ware', 'Amari Cooper'], 1)


@ntools.raises(ConstraintConflictException)
def test_dup_group_rule2():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Eli Manning', 'Russell Wilson', 'Doug Martin'],
                             (1, 2))
    lcs.add_group_constraint(['Eli Manning', 'Russell Wilson', 'Doug Martin'],
                             (1, 2))


@ntools.raises(ConstraintException)
def test_bad_group_shadow_lock_bound():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Spencer Ware', 'Amari Cooper'], 2)


@ntools.raises(ConstraintException)
def test_bad_group_shadow_lock_hi_lo_bound():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Spencer Ware', 'Amari Cooper'], (2, 2))


@ntools.raises(ConstraintException)
def test_bad_group_shadow_ban_bound():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Spencer Ware', 'Amari Cooper'], 0)


@ntools.raises(ConstraintException)
def test_bad_group_shadow_ban_hi_lo_bound():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Spencer Ware', 'Amari Cooper'], (0, 0))


@ntools.raises(ConstraintException)
def test_bad_group_duplicate_bounds():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Spencer Ware', 'Amari Cooper'], (1, 1))


@ntools.raises(ConstraintException)
def test_bad_group_negative_min():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Spencer Ware', 'Amari Cooper'], (-1, 1))


@ntools.raises(ConstraintException)
def test_bad_group_zero_min():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Spencer Ware', 'Amari Cooper'], (0, 1))


@ntools.raises(ConstraintException)
def test_bad_group_max():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Spencer Ware', 'Amari Cooper'], 3)


@ntools.raises(ConstraintException)
def test_bad_group_max_set():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Spencer Ware', 'Amari Cooper'], (1, 3))


@ntools.raises(ConstraintException)
def test_bad_group_dup_player():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Amari Cooper', 'Amari Cooper'], 1)


@ntools.raises(ConstraintException)
def test_bad_group_bounds_type():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Spencer Ware', 'Amari Cooper'], '1')


@ntools.raises(ConstraintException)
def test_bad_group_too_many_bounds():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Spencer Ware', 'Amari Cooper'], (1, 1, 2))


@ntools.raises(ConstraintException)
def test_single_player_group():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Spencer Ware'], 1)


@ntools.raises(ConstraintException)
def test_empty_group():
    lcs = LineupConstraints()
    lcs.add_group_constraint([], 1)


@ntools.raises(ConstraintException)
def test_empty_lock():
    lcs = LineupConstraints()
    lcs.lock([])


@ntools.raises(ConstraintException)
def test_empty_ban():
    lcs = LineupConstraints()
    lcs.ban([])


@ntools.raises(ConstraintConflictException)
def test_ban_lock_conflict():
    lcs = LineupConstraints()
    lcs.lock(['Will Fuller'])
    lcs.ban(['Will Fuller'])


@ntools.raises(ConstraintConflictException)
def test_lock_ban_conflict():
    lcs = LineupConstraints()
    lcs.ban(['Will Fuller'])
    lcs.lock(['Will Fuller'])


@ntools.raises(ConstraintConflictException)
def test_lock_group_conflict():
    lcs = LineupConstraints()
    lcs.lock(['Eli Manning'])
    lcs.add_group_constraint(['Eli Manning', 'Doug Martin'], (1, 2))


@ntools.raises(ConstraintConflictException)
def test_group_lock_conflict():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Eli Manning', 'Doug Martin'], (1, 2))
    lcs.lock(['Eli Manning'])


@ntools.raises(ConstraintConflictException)
def test_ban_group_conflict():
    lcs = LineupConstraints()
    lcs.ban(['Eli Manning'])
    lcs.add_group_constraint(['Eli Manning', 'Doug Martin'], (1, 2))


@ntools.raises(ConstraintConflictException)
def test_group_ban_conflict():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Eli Manning', 'Doug Martin'], (1, 2))
    lcs.ban(['Eli Manning'])
