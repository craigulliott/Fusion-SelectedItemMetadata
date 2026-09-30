"""How describe() combines subjects and traits, independent of any real fact."""

import unittest
from unittest import mock

import _bootstrap  # noqa: F401

import adsk.core
import adsk.fusion
import fakes
from lib import describe as describe_module
from lib.describe import Trait, describe


def _text(value):
    return lambda entity: value


def _broken(entity):
    raise ValueError("boom")


def _with_tables(subjects, traits):
    return mock.patch.multiple(describe_module, SUBJECTS=subjects, TRAITS=traits)


class DescribeTest(unittest.TestCase):
    def setUp(self):
        adsk.core.Application.logged.clear()
        self.point = fakes.FakeSketchPoint(fakes.FakeSketch("Sketch1"))

    def test_the_subject_comes_first_then_traits_in_table_order(self):
        traits = [
            Trait(adsk.fusion.SketchEntity, _text(True), _text("first trait")),
            Trait(adsk.fusion.SketchPoint, _text(True), _text("second trait")),
        ]
        with _with_tables({adsk.fusion.SketchPoint: _text("subject")}, traits):
            self.assertEqual(describe(self.point), ["subject", "first trait", "second trait"])

    def test_only_the_most_specific_subject_applies(self):
        subjects = {adsk.fusion.SketchEntity: _text("entity"), adsk.fusion.SketchPoint: _text("point")}
        line = fakes.FakeSketchLine(fakes.FakeSketch("Sketch1"))
        with _with_tables(subjects, []):
            self.assertEqual(describe(self.point), ["point"])
            self.assertEqual(describe(line), ["entity"])

    def test_a_trait_applies_to_subclasses_of_its_type(self):
        with _with_tables({}, [Trait(adsk.fusion.SketchEntity, _text(True), _text("sketch entity trait"))]):
            self.assertEqual(describe(self.point), ["sketch entity trait"])

    def test_a_trait_adds_nothing_when_its_condition_does_not_hold(self):
        with _with_tables({}, [Trait(adsk.fusion.SketchEntity, _text(False), _text("never"))]):
            self.assertEqual(describe(self.point), [])

    def test_a_failure_costs_only_its_own_part_and_is_reported(self):
        traits = [
            Trait(adsk.fusion.SketchEntity, _text(True), _broken),
            Trait(adsk.fusion.SketchEntity, _broken, _text("never")),
            Trait(adsk.fusion.SketchEntity, _text(True), _text("kept")),
        ]
        with _with_tables({adsk.fusion.SketchPoint: _broken}, traits):
            self.assertEqual(describe(self.point), ["kept"])
        self.assertEqual(len(adsk.core.Application.logged), 3)
        self.assertTrue(all("_broken" in message for message in adsk.core.Application.logged))

    def test_an_entity_nothing_applies_to_gets_no_text(self):
        self.assertEqual(describe(adsk.fusion.BRepEdge()), [])


if __name__ == "__main__":
    unittest.main()
