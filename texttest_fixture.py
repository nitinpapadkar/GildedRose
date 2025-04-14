# -*- coding: utf-8 -*-
from __future__ import print_function
import unittest
from copy import deepcopy
from gilded_rose import GildedRose, Item


class GildedRoseSimulationTest(unittest.TestCase):        

    def simulate_days(self, days, initial_items, expected_results_day):
        print(f"📦 Running simulation for {days} day...\n")
        items = deepcopy(initial_items)
        gr = GildedRose(items)

        for _ in range(days):
            gr.update_quality()

        # Mapping for easier matching
        name_map = {
            "+5 Dexterity Vest": "+5 Dexterity Vest",
            "Aged Brie": "Aged Brie",
            "Elixir of the Mongoose": "Elixir of the Mongoose",
            "Sulfuras, Hand of Ragnaros": "Sulfuras, Hand of Ragnaros",
            "Sulfuras, Hand of Ragnaros (negative)": "Sulfuras, Hand of Ragnaros",
            "Backstage 15 days": "Backstage passes to a TAFKAL80ETC concert",
            "Backstage 10 days": "Backstage passes to a TAFKAL80ETC concert",
            "Backstage 5 days": "Backstage passes to a TAFKAL80ETC concert",
            "Conjured Mana Cake": "Conjured Mana Cake",
        }

        # Disambiguate duplicate names for matching
        used = {}
        for item in items:
            for key, name in name_map.items():
                if item.name == name and key not in used:
                    expected = expected_results_day[key]
                    with self.subTest(item=item.name, key=key):
                        print(f"🔍 Testing {key}")
                        print(f"   Expected: sell_in={expected['sell_in']}, quality={expected['quality']}")
                        print(f"   Actual:   sell_in={item.sell_in}, quality={item.quality}")
                        try:
                            self.assertEqual(item.sell_in, expected["sell_in"], f"SellIn mismatch for {key}")
                            self.assertEqual(item.quality, expected["quality"], f"Quality mismatch for {key}")
                            print(" ✅ Test passed.\n")
                        except AssertionError as e:
                            print(" ❌ Test failed.\n")
                        used[key] = True
                        break



def main():
    # Original items
    initial_items = [
                        Item(name="+5 Dexterity Vest", sell_in=10, quality=20),
                        Item(name="Aged Brie", sell_in=2, quality=0),
                        Item(name="Elixir of the Mongoose", sell_in=5, quality=7),
                        Item(name="Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
                        Item(name="Sulfuras, Hand of Ragnaros (negative)", sell_in=-1, quality=80),
                        Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=20),
                        Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=49),
                        Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=49),
                        Item(name="Conjured Mana Cake", sell_in=3, quality=6),
                    ]


    # Expected values after 1 day
    expected_results_day_1 = {
                                "+5 Dexterity Vest": {"sell_in": 9, "quality": 19},  # -1 sell_in, -1 quality
                                "Aged Brie": {"sell_in": 1, "quality": 1},           # +1 quality (max 50)
                                "Elixir of the Mongoose": {"sell_in": 4, "quality": 6},
                                "Sulfuras, Hand of Ragnaros": {"sell_in": 0, "quality": 80},          # No change
                                "Sulfuras, Hand of Ragnaros (negative)": {"sell_in": -1, "quality": 80},        # No change
                                "Backstage 15 days": {"sell_in": 14, "quality": 21},       # >10 days left, +1
                                "Backstage 10 days": {"sell_in": 9, "quality": 50},        # 10 or less, +2 → capped at 50
                                "Backstage 5 days": {"sell_in": 4, "quality": 50},         # 5 or less, +3 → capped at 50
                                "Conjured Mana Cake": {"sell_in": 2, "quality": 4},            # -2 quality (double decay)
                            }

    # Expected results after 10 days
        # After 10 days simulation, we apply rules like:
        # Normal items: -1 quality/day; after sell-in, -2/day.
        # Conjured items: -2/day; after sell-in, -4/day.
        # Aged Brie: +1/day; after sell-in, +2/day.
        # Backstage:
            # +1 (>10 days)
            # +2 (10–6 days)
            # +3 (5–1 days)

        # Drop to 0 at sell-in 0 or less.
    expected_results_day_10 = {
                                "+5 Dexterity Vest": {"sell_in": 0, "quality": 10},  # -1/day
                                "Aged Brie": {"sell_in": -8, "quality": 18},         # 2 days +1, 8 days +2 → 18
                                "Elixir of the Mongoose": {"sell_in": -5, "quality": 0},  # Decays to 0
                                "Sulfuras, Hand of Ragnaros": {"sell_in": 0, "quality": 80},
                                "Sulfuras, Hand of Ragnaros (negative)": {"sell_in": -1, "quality": 80},
                                "Backstage 15 days": {"sell_in": 5, "quality": 35},  # Days: +1, +1, +1, +2, +2, +2, +2, +3, +3, +3 = +15
                                "Backstage 10 days": {"sell_in": 0, "quality": 0},   # Day 10 ends with sell_in=0 → drops to 0
                                "Backstage 5 days": {"sell_in": -5, "quality": 0},   # Passed sell-in, quality = 0
                                "Conjured Mana Cake": {"sell_in": -7, "quality": 0},     # 3 days: -2; 7 days: -4 → reaches 0
                            }

    print("🔁 Starting Gilded Rose Simulation Tests\n")

    simObj = GildedRoseSimulationTest()

    # Run simulations
    print("*************** 📦 Running Day 1 Simulation *****************\n")
    simObj.simulate_days(1, initial_items, expected_results_day_1)

    print("***************  📦 Running Day 10 Simulation ***************\n")
    simObj.simulate_days(10, initial_items, expected_results_day_10)

    print("✅ All simulations complete.\n")


if __name__ == '__main__':
    main()
