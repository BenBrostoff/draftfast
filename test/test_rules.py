from rules import RuleSet, RuleConflictException, RuleException
from nose import tools as ntool


def test_dup_group_rule():
    rs = RuleSet()
    rs.add_group_rule(['Spencer Ware', 'Amari Cooper'], 1)
    rs.add_group_rule(['Spencer Ware', 'Amari Cooper'], 1)

    ntool.assert_equal(len(rs), 1)

    rs.add_group_rule(['Eli Manning', 'Russell Wilson', 'Doug Martin'], 0)
    rs.add_group_rule(['Eli Manning', 'Russell Wilson', 'Doug Martin'], 0)

    ntool.assert_equal(len(rs), 2)


def test_multi_lock_multi_ban():
    rs = RuleSet()
    rs.add_group_rule(['Spencer Ware', 'Amari Cooper'], 2)
    rs.add_group_rule(['Eli Manning', 'Russell Wilson', 'Doug Martin'], 0)

    ntool.assert_equal(len(rs), 2)


@ntool.raises(RuleException)
def test_bad_group0():
    rs = RuleSet()
    rs.add_group_rule(['Spencer Ware', 'Amari Cooper'], (1, 1))


@ntool.raises(RuleException)
def test_bad_group1():
    rs = RuleSet()
    rs.add_group_rule(['Spencer Ware', 'Amari Cooper'], (-1, 1))


@ntool.raises(RuleException)
def test_bad_group2():
    rs = RuleSet()
    rs.add_group_rule(['Spencer Ware', 'Amari Cooper'], (1, 3))


@ntool.raises(RuleException)
def test_bad_group3():
    rs = RuleSet()
    rs.add_group_rule(['Spencer Ware', 'Amari Cooper'], (0, 1))


@ntool.raises(RuleException)
def test_bad_group4():
    rs = RuleSet()
    rs.add_group_rule(['Amari Cooper', 'Amari Cooper'], 1)


@ntool.raises(RuleException)
def test_bad_group5():
    rs = RuleSet()
    rs.add_group_rule(['Spencer Ware', 'Amari Cooper'], '1')


@ntool.raises(RuleException)
def test_bad_group6():
    rs = RuleSet()
    rs.add_group_rule(['Spencer Ware', 'Amari Cooper'], (1, 1, 2))


@ntool.raises(RuleException)
def test_bad_group7():
    rs = RuleSet()
    rs.add_group_rule([], 1)


@ntool.raises(RuleException)
def test_bad_group8():
    rs = RuleSet()
    rs.add_group_rule(['Spencer Ware', 'Amari Cooper'], 3)


def test_build_ruleset():
    rs = RuleSet()
    rs.add_group_rule(['Spencer Ware', 'Amari Cooper'], 1)
    rs.add_ban_rule(['Packers'])
    rs.add_group_rule(['Eli Manning', 'Russell Wilson', 'Doug Martin'],
                      (1, 3))
    rs.add_lock_rule(['Will Fuller'])


def test_ruleset_eq():
    rs1 = RuleSet()
    rs1.add_group_rule(['Spencer Ware', 'Amari Cooper'], 1)
    rs1.add_ban_rule(['Packers'])
    rs1.add_group_rule(['Eli Manning', 'Russell Wilson', 'Doug Martin'],
                       (1, 3))
    rs1.add_lock_rule(['Will Fuller'])

    rs2 = RuleSet()
    rs2.add_group_rule(['Spencer Ware', 'Amari Cooper'], 1)
    rs2.add_ban_rule(['Packers'])
    rs2.add_group_rule(['Eli Manning', 'Russell Wilson', 'Doug Martin'],
                       (1, 3))
    rs2.add_lock_rule(['Will Fuller'])

    ntool.assert_equal(rs1, rs2)


def test_rule_aliasing():
    rs1 = RuleSet()
    rs1.add_group_rule(['Spencer Ware', 'Amari Cooper'], 1)
    rs1.add_ban_rule(['Packers'])
    rs1.add_group_rule(['Eli Manning', 'Russell Wilson', 'Doug Martin'],
                       (1, 3))
    rs1.add_lock_rule(['Will Fuller'])

    rs2 = RuleSet()
    rs2.add_group_rule(['Eli Manning', 'Russell Wilson', 'Doug Martin'],
                       (1, 3))
    rs2.add_group_rule(['Will Fuller'], 1)
    rs2.add_group_rule(['Spencer Ware', 'Amari Cooper'], 1)
    rs2.add_group_rule(['Packers'], 0)

    ntool.assert_equal(rs1, rs2)


def test_duplicate_rules():
    rs1 = RuleSet()
    rs1.add_group_rule(['Spencer Ware', 'Amari Cooper'], 1)
    rs1.add_ban_rule(['Packers'])
    rs1.add_group_rule(['Eli Manning', 'Russell Wilson', 'Doug Martin'],
                       (1, 3))
    rs1.add_lock_rule(['Will Fuller'])

    rs2 = RuleSet()
    rs2.add_group_rule(['Eli Manning', 'Russell Wilson', 'Doug Martin'],
                       (1, 3))
    rs2.add_lock_rule(['Will Fuller'])
    rs2.add_group_rule(['Spencer Ware', 'Amari Cooper'], 1)
    rs2.add_ban_rule(['Packers'])
    rs2.add_group_rule(['Eli Manning', 'Russell Wilson', 'Doug Martin'],
                       (1, 3))
    rs2.add_group_rule(['Will Fuller'], 1)
    rs2.add_group_rule(['Spencer Ware', 'Amari Cooper'], 1)
    rs2.add_group_rule(['Packers'], 0)
    rs2.add_group_rule(['Eli Manning', 'Doug Martin', 'Russell Wilson'],
                       (1, 3))

    ntool.assert_equal(rs1, rs2)


@ntool.raises(RuleConflictException)
def test_ban_lock_conflict():
    rs = RuleSet()
    rs.add_lock_rule(['Will Fuller'])
    rs.add_ban_rule(['Will Fuller'])


@ntool.raises(RuleConflictException)
def test_lock_group_conflict():
    rs = RuleSet()
    rs.add_lock_rule(['Eli Manning'])
    rs.add_group_rule(['Eli Manning', 'Doug Martin'], (1, 2))


@ntool.raises(RuleConflictException)
def test_ban_group_conflict():
    rs = RuleSet()
    rs.add_ban_rule(['Eli Manning'])
    rs.add_group_rule(['Eli Manning', 'Doug Martin'], (1, 2))
