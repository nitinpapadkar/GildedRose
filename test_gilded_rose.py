# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose, AddItem


class GildedRoseTest(unittest.TestCase):
    def test_foo(self):
        items = [AddItem("Normal", 0, 60)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("Normal", items[0].name)

        
if __name__ == '__main__':
    unittest.main()