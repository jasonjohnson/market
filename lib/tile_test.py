import unittest

from lib import base, tile, harvester


class TileTest(unittest.TestCase):
    def test_tile_capacity(self):
        t = tile.Tile(row=0, column=0)

        b = base.Base(starting_spice=1)
        h0 = harvester.Harvester(b)

        self.assertTrue(t.has_unit_capacity())

        t.add_unit(h0)

        self.assertFalse(t.has_unit_capacity())

        t.remove_unit(h0)

        self.assertTrue(t.has_unit_capacity())
