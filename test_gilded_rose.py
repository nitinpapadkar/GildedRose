# -*- coding: utf-8 -*-
import unittest
from gilded_rose import Item, GildedRose

# Define test cases as dictionaries
test_cases = [
    {
        "name": "Normal item degrades before sell date",
        "item": {"name": "Elixir of the Mongoose", "sell_in": 5, "quality": 10},
        "expected": {"sell_in": 4, "quality": 9}
    },
    {
        "name": "Normal item degrades twice as fast after sell date",
        "item": {"name": "Elixir of the Mongoose", "sell_in": 0, "quality": 10},
        "expected": {"sell_in": -1, "quality": 8}
    },
    {
        "name": "Normal item quality never negative",
        "item": {"name": "Elixir of the Mongoose", "sell_in": 5, "quality": 0},
        "expected": {"sell_in": 4, "quality": 0}
    },
    {
        "name": "Aged Brie increases in quality",
        "item": {"name": "Aged Brie", "sell_in": 2, "quality": 0},
        "expected": {"sell_in": 1, "quality": 1}
    },
    {
        "name": "Aged Brie max quality is 50",
        "item": {"name": "Aged Brie", "sell_in": 2, "quality": 50},
        "expected": {"sell_in": 1, "quality": 50}
    },
    {
        "name": "Sulfuras never changes",
        "item": {"name": "Sulfuras, Hand of Ragnaros", "sell_in": 0, "quality": 80},
        "expected": {"sell_in": 0, "quality": 80}
    },
    {
        "name": "Backstage pass increases by 1 (>10 days)",
        "item": {"name": "Backstage passes to a TAFKAL80ETC concert", "sell_in": 15, "quality": 20},
        "expected": {"sell_in": 14, "quality": 21}
    },
    {
        "name": "Backstage pass increases by 2 (10 days)",
        "item": {"name": "Backstage passes to a TAFKAL80ETC concert", "sell_in": 10, "quality": 20},
        "expected": {"sell_in": 9, "quality": 22}
    },
    {
        "name": "Backstage pass increases by 3 (5 days)",
        "item": {"name": "Backstage passes to a TAFKAL80ETC concert", "sell_in": 5, "quality": 20},
        "expected": {"sell_in": 4, "quality": 23}
    },
    {
        "name": "Backstage pass drops to 0 after concert",
        "item": {"name": "Backstage passes to a TAFKAL80ETC concert", "sell_in": 0, "quality": 20},
        "expected": {"sell_in": -1, "quality": 0}
    },
    {
        "name": "Conjured item degrades twice as fast",
        "item": {"name": "Conjured Mana Cake", "sell_in": 3, "quality": 6},
        "expected": {"sell_in": 2, "quality": 4}
    },
    {
        "name": "Conjured item degrades by 4 after sell date",
        "item": {"name": "Conjured Mana Cake", "sell_in": 0, "quality": 6},
        "expected": {"sell_in": -1, "quality": 2}
    },
    {
        "name": "Conjured item quality never negative",
        "item": {"name": "Conjured Mana Cake", "sell_in": 3, "quality": 1},
        "expected": {"sell_in": 2, "quality": 0}
    }
]


class GildedRoseTest(unittest.TestCase):

    def test_all_cases(self):
        for case in test_cases:
            with self.subTest(case=case["name"]):
                item_data = case["item"]
                expected = case["expected"]
                item = Item(item_data["name"], item_data["sell_in"], item_data["quality"])
                gilded_rose = GildedRose([item])
                gilded_rose.update_quality()

                print(f"\n--- Running test: {case['name']} ---")
                print(f"Before update: sell_in={item_data['sell_in']}, quality={item_data['quality']}")
                print(f"Expected: sell_in={expected['sell_in']}, quality={expected['quality']}")
                print(f"Actual:   sell_in={item.sell_in}, quality={item.quality}")

                try:
                    self.assertEqual(expected["sell_in"], item.sell_in, f"Failed SellIn for: {case['name']}")
                    self.assertEqual(expected["quality"], item.quality, f"Failed Quality for: {case['name']}")
                    print("✅ Test passed.")
                except AssertionError as e:
                    print("❌ Test failed.")
                    raise e


if __name__ == '__main__':
    unittest.main()
