# -*- coding: utf-8 -*-
from __future__ import print_function
import unittest
from copy import deepcopy
from gilded_rose import GildedRose, AddItem


class GildedRoseSimulationTest(unittest.TestCase):        

    def simulate_days(self, days, items, expected_results_day):
        print(f"📦 Running simulation for {days} day...\n")
        gr = GildedRose(items)

        for _ in range(days):
            gr.update_quality()        
       
        for item in items:
            expected = expected_results_day[item.name]
            print(f"🔍 Testing {item.name}")
            print(f"   Expected: sell_in={expected['sell_in']}, quality={expected['quality']}")
            print(f"   Actual:   sell_in={item.sell_in}, quality={item.quality}")
            try:
                self.assertEqual(item.sell_in, expected["sell_in"], f"SellIn mismatch for {item.name}")
                self.assertEqual(item.quality, expected["quality"], f"Quality mismatch for {item.name}")
                print(" ✅ Test passed.\n")
            except AssertionError as e:
                print(" ❌ Test failed.\n")
            
def main():
    # Original items
    initial_items = [
                        AddItem(name="Normal", sell_in=10, quality=20), #Normal Item - Quality decreases, Once the sell by date has passed, Quality degrades twice as fast
                        AddItem(name="Aged Brie", sell_in=5, quality=0), #Aged Brie - increases in Quality the older it gets
                        AddItem(name="Sulfuras", sell_in=0, quality=80), #never has to be sold or decreases in Quality
                        AddItem(name="Backstage passes", sell_in=15, quality=15),
                        AddItem(name="Conjured", sell_in=10, quality=40),
                    ]


    # Expected results after X days
        # After X days simulation, we apply rules like:
        # Normal items: -1 quality/day; after sell-in, -2/day.
        # Conjured items: -2/day; after sell-in, -4/day.
        # Aged Brie: +1/day; after sell-in, +2/day.
        # Backstage:
            # +1 (>10 days)
            # +2 (10–6 days)
            # +3 (5–1 days)
            # 0 after sell-in
        # Drop to 0 at sell-in 0 or less.

    # Expected values after 1 day
    expected_results_day_1 = {
                                "Normal": {"sell_in": 9, "quality": 19},  # -1 sell_in, -1 quality
                                "Aged Brie": {"sell_in": 4, "quality": 1}, # -1 sell_in,+1 quality (max 50)
                                "Sulfuras": {"sell_in": 0, "quality": 80}, # No change
                                "Backstage passes": {"sell_in": 14, "quality": 16}, # -1 sell_in, >10 days left -> +1
                                "Conjured": {"sell_in": 9, "quality": 38}, # -1 sell_in, +2 quality (max 50)
                            }

    
    expected_results_day_5 = {
                                "Normal": {"sell_in": 5, "quality": 15},  # -1 sell_in, -1 quality
                                "Aged Brie": {"sell_in": 0, "quality": 5}, # -1 sell_in,+1 quality (max 50)
                                "Sulfuras": {"sell_in": 0, "quality": 80}, # No change
                                "Backstage passes": {"sell_in": 10, "quality": 21}, # -1 sell_in, >10 days left -> +1
                                "Conjured": {"sell_in": 5, "quality": 30}, # -1 sell_in, +2 quality (max 50)
                            }
    
    expected_results_day_10 = {
                                "Normal": {"sell_in": 0, "quality": 10},  # -1 sell_in, -1 quality
                                "Aged Brie": {"sell_in": -5, "quality": 15}, # -1 sell_in,+1 quality (max 50)
                                "Sulfuras": {"sell_in": 0, "quality": 80}, # No change
                                "Backstage passes": {"sell_in": 5, "quality": 32}, # -1 sell_in, >10 days left -> +1
                                "Conjured": {"sell_in": 0, "quality": 20}, # -1 sell_in, +2 quality (max 50)
                            }

    expected_results_day_15 = {
                                "Normal": {"sell_in": -5, "quality": 0},  # -1 sell_in, -1 quality
                                "Aged Brie": {"sell_in": -10, "quality": 25}, # -1 sell_in,+1 quality (max 50)
                                "Sulfuras": {"sell_in": 0, "quality": 80}, # No change
                                "Backstage passes": {"sell_in": 0, "quality": 47}, # -1 sell_in, >10 days left -> +1
                                "Conjured": {"sell_in": -5, "quality": 0}, # -1 sell_in, +2 quality (max 50)
                            }
    
    expected_results_day_20 = {
                                "Normal": {"sell_in": -10, "quality": 0},  # -1 sell_in, -1 quality
                                "Aged Brie": {"sell_in": -15, "quality": 35}, # -1 sell_in,+1 quality (max 50)
                                "Sulfuras": {"sell_in": 0, "quality": 80}, # No change
                                "Backstage passes": {"sell_in": -5, "quality": 0}, # -1 sell_in, >10 days left -> +1
                                "Conjured": {"sell_in": -10, "quality": 0}, # -1 sell_in, +2 quality (max 50)
                            }
    
    print("\n 🔁 Starting Gilded Rose Simulation Tests\n")
    simObj = GildedRoseSimulationTest()


    # Menu-driven Test simulation
    print("Choose a simulation to run:")
    print("1. Run Simulation test for 1 day")
    print("2. Run Simulation test for 5 days")
    print("3. Run Simulation test for 10 days")
    print("4. Run Simulation test for 20 days")
    print("Enter your choice:")

    choice = input().strip()

    if choice == "1":
        print("*************** 📦 Running Day 1 Simulation *****************\n")
        simObj.simulate_days(1, initial_items, expected_results_day_1)
    elif choice == "2":
        print("*************** 📦 Running Day 5 Simulation *****************\n")
        simObj.simulate_days(5, initial_items, expected_results_day_5)
    elif choice == "3":
        print("*************** 📦 Running Day 10 Simulation *****************\n")
        simObj.simulate_days(10, initial_items, expected_results_day_10)
    elif choice == "4":
        print("*************** 📦 Running Day 20 Simulation *****************\n")
        simObj.simulate_days(20, initial_items, expected_results_day_20)
    else:
        print("Invalid choice! ..\n")

    print("✅ simulations complete.\n")



if __name__ == '__main__':
    main()
