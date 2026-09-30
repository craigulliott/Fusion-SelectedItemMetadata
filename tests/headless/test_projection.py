"""The projection trait, through the real tables."""

import unittest

import _bootstrap  # noqa: F401

import adsk.core
import adsk.fusion
import fakes
from lib.describe import describe


class ProjectionTest(unittest.TestCase):
    def setUp(self):
        adsk.core.Application.logged.clear()
        self.sketch = fakes.FakeSketch("Side Profile")
        self.source_sketch = fakes.FakeSketch("Bellows Barrel")

    def test_a_point_projected_from_a_sketch_names_that_sketch(self):
        source = fakes.FakeSketchPoint(self.source_sketch)
        point = fakes.FakeSketchPoint(self.sketch, source=source)
        self.assertEqual(describe(point), ["projected from sketch 'Bellows Barrel'"])

    def test_a_line_projected_from_a_sketch_names_that_sketch(self):
        source = fakes.FakeSketchLine(self.source_sketch)
        line = fakes.FakeSketchLine(self.sketch, source=source)
        self.assertEqual(describe(line), ["projected from sketch 'Bellows Barrel'"])

    def test_an_entity_that_is_not_projected_gets_no_text(self):
        self.assertEqual(describe(fakes.FakeSketchPoint(self.sketch)), [])
        self.assertEqual(adsk.core.Application.logged, [])

    def test_a_projection_fusion_cannot_resolve_gets_no_text_and_is_not_reported(self):
        endpoint = fakes.FakeSketchPoint(self.sketch, unresolvable=True)
        self.assertEqual(describe(endpoint), [])
        self.assertEqual(adsk.core.Application.logged, [])

    def test_a_projection_from_anything_but_a_sketch_gets_no_text(self):
        point = fakes.FakeSketchPoint(self.sketch, source=adsk.fusion.BRepEdge())
        self.assertEqual(describe(point), [])


if __name__ == "__main__":
    unittest.main()
