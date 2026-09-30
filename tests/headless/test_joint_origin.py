"""The joint origin subject and the component trait, through the real tables."""

import unittest

import _bootstrap  # noqa: F401

import fakes
from lib.describe import describe


class JointOriginTest(unittest.TestCase):
    def setUp(self):
        self.design = fakes.FakeDesign()

    def test_a_joint_origin_in_the_root_component_shows_only_its_name(self):
        origin = fakes.FakeJointOrigin("Thread", self.design.rootComponent)
        self.assertEqual(describe(origin), ["Joint origin 'Thread'"])

    def test_a_joint_origin_in_a_component_also_names_the_component(self):
        bracket = fakes.FakeComponent("Bracket", self.design)
        origin = fakes.FakeJointOrigin("Mount Origin", bracket)
        self.assertEqual(describe(origin), ["Joint origin 'Mount Origin'", "in component 'Bracket'"])


if __name__ == "__main__":
    unittest.main()
