from draftfast.lineup_contraints import (LineupConstraints,
                                         ConstraintConflictException,
                                         ConstraintException)
from nose import tools as ntool


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

    ntool.assert_equal(lcs1, lcs2)


def test_build_constraint_set():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Spencer Ware', 'Amari Cooper'], 1)
    lcs.ban(['Packers'])
    lcs.add_group_constraint(['Eli Manning', 'Russell Wilson', 'Doug Martin'],
                             (1, 3))
    lcs.lock(['Will Fuller'])

    # locked and banned players don't count towards length
    ntool.assert_equal(len(lcs), 2)


@ntool.raises(ConstraintConflictException)
def test_dup_group_rule():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Spencer Ware', 'Amari Cooper'], 1)
    lcs.add_group_constraint(['Spencer Ware', 'Amari Cooper'], 1)


@ntool.raises(ConstraintConflictException)
def test_dup_group_rule2():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Eli Manning', 'Russell Wilson', 'Doug Martin'],
                             (1, 2))
    lcs.add_group_constraint(['Eli Manning', 'Russell Wilson', 'Doug Martin'],
                             (1, 2))


@ntool.raises(ConstraintException)
def test_bad_group_shadow_lock_bound():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Spencer Ware', 'Amari Cooper'], 2)


@ntool.raises(ConstraintException)
def test_bad_group_shadow_lock_hi_lo_bound():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Spencer Ware', 'Amari Cooper'], (2, 2))


@ntool.raises(ConstraintException)
def test_bad_group_shadow_ban_bound():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Spencer Ware', 'Amari Cooper'], 0)


@ntool.raises(ConstraintException)
def test_bad_group_shadow_ban_hi_lo_bound():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Spencer Ware', 'Amari Cooper'], (0, 0))


@ntool.raises(ConstraintException)
def test_bad_group_duplicate_bounds():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Spencer Ware', 'Amari Cooper'], (1, 1))


@ntool.raises(ConstraintException)
def test_bad_group_negative_min():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Spencer Ware', 'Amari Cooper'], (-1, 1))


@ntool.raises(ConstraintException)
def test_bad_group_zero_min():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Spencer Ware', 'Amari Cooper'], (0, 1))


@ntool.raises(ConstraintException)
def test_bad_group_max():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Spencer Ware', 'Amari Cooper'], 3)


@ntool.raises(ConstraintException)
def test_bad_group_max_set():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Spencer Ware', 'Amari Cooper'], (1, 3))


@ntool.raises(ConstraintException)
def test_bad_group_dup_player():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Amari Cooper', 'Amari Cooper'], 1)


@ntool.raises(ConstraintException)
def test_bad_group_bounds_type():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Spencer Ware', 'Amari Cooper'], '1')


@ntool.raises(ConstraintException)
def test_bad_group_too_many_bounds():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Spencer Ware', 'Amari Cooper'], (1, 1, 2))


@ntool.raises(ConstraintException)
def test_single_player_group():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Spencer Ware'], 1)


@ntool.raises(ConstraintException)
def test_empty_group():
    lcs = LineupConstraints()
    lcs.add_group_constraint([], 1)


@ntool.raises(ConstraintException)
def test_empty_lock():
    lcs = LineupConstraints()
    lcs.lock([])


@ntool.raises(ConstraintException)
def test_empty_ban():
    lcs = LineupConstraints()
    lcs.ban([])


@ntool.raises(ConstraintConflictException)
def test_ban_lock_conflict():
    lcs = LineupConstraints()
    lcs.lock(['Will Fuller'])
    lcs.ban(['Will Fuller'])


@ntool.raises(ConstraintConflictException)
def test_lock_ban_conflict():
    lcs = LineupConstraints()
    lcs.ban(['Will Fuller'])
    lcs.lock(['Will Fuller'])


@ntool.raises(ConstraintConflictException)
def test_lock_group_conflict():
    lcs = LineupConstraints()
    lcs.lock(['Eli Manning'])
    lcs.add_group_constraint(['Eli Manning', 'Doug Martin'], (1, 2))


@ntool.raises(ConstraintConflictException)
def test_group_lock_conflict():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Eli Manning', 'Doug Martin'], (1, 2))
    lcs.lock(['Eli Manning'])


@ntool.raises(ConstraintConflictException)
def test_ban_group_conflict():
    lcs = LineupConstraints()
    lcs.ban(['Eli Manning'])
    lcs.add_group_constraint(['Eli Manning', 'Doug Martin'], (1, 2))


@ntool.raises(ConstraintConflictException)
def test_group_ban_conflict():
    lcs = LineupConstraints()
    lcs.add_group_constraint(['Eli Manning', 'Doug Martin'], (1, 2))
    lcs.ban(['Eli Manning'])
