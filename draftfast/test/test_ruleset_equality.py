import unittest
from draftfast.rules import RuleSet


assertions = unittest.TestCase("__init__")


def test_ruleset_equality():
    ruleset_a = RuleSet(
        site='a', league='b', roster_size=1, position_limits=[], salary_max=1
    )
    ruleset_b = RuleSet(
        site='a', league='b', roster_size=1, position_limits=[], salary_max=1
    )
    assertions.assertEqual(ruleset_a, ruleset_b)
