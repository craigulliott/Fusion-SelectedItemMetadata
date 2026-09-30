"""Sharing Fusion's status line with its own selection readout."""

import unittest

import _bootstrap  # noqa: F401

import fakes
from lib import status

POINT_READOUT = "1 Sketch Point"
EDGE_READOUT = "1 Edge | Length : 30.00 mm"


class StatusTest(unittest.TestCase):
    def setUp(self):
        # The module keeps state between calls, as it does in Fusion.
        status.restore(fakes.FakeUI())
        self.ui = fakes.FakeUI(POINT_READOUT)

    def test_our_text_follows_fusions_readout(self):
        status.show(self.ui, ["projected from sketch 'A'"])
        self.assertEqual(self.ui.statusMessage, "1 Sketch Point | projected from sketch 'A'")

    def test_without_a_readout_our_text_stands_alone(self):
        ui = fakes.FakeUI("")
        status.show(ui, ["Joint origin 'Thread'"])
        self.assertEqual(ui.statusMessage, "Joint origin 'Thread'")

    def test_our_own_text_is_not_mistaken_for_a_new_readout(self):
        status.show(self.ui, ["first"])
        status.show(self.ui, ["second"])
        self.assertEqual(self.ui.statusMessage, "1 Sketch Point | second")

    def test_a_new_readout_replaces_the_previous_one(self):
        status.show(self.ui, ["first"])
        self.ui.statusMessage = EDGE_READOUT   # Fusion, on the next selection
        status.show(self.ui, ["second"])
        self.assertEqual(self.ui.statusMessage, "1 Edge | Length : 30.00 mm | second")

    def test_nothing_to_add_puts_the_bare_readout_back(self):
        status.show(self.ui, ["first"])
        status.show(self.ui, [])
        self.assertEqual(self.ui.statusMessage, POINT_READOUT)

    def test_nothing_to_add_leaves_fusions_readout_untouched(self):
        status.show(self.ui, [])
        self.assertEqual(self.ui.writes, 0)

    def test_restore_puts_the_readout_back_while_our_text_shows(self):
        status.show(self.ui, ["first"])
        status.restore(self.ui)
        self.assertEqual(self.ui.statusMessage, POINT_READOUT)

    def test_restore_leaves_a_newer_readout_alone(self):
        status.show(self.ui, ["first"])
        self.ui.statusMessage = EDGE_READOUT
        writes = self.ui.writes
        status.restore(self.ui)
        self.assertEqual((self.ui.statusMessage, self.ui.writes), (EDGE_READOUT, writes))


if __name__ == "__main__":
    unittest.main()
