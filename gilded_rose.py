# -*- coding: utf-8 -*-

# Main GildedRose system class that processes a list of items
class GildedRose(object):
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        # Update quality for each item using appropriate strategy
        for item in self.items:
            updater = ItemUpdaterFactory.get_updater(item)
            updater.update()
            ItemQualityRules.apply_limits(item)  # Enforce global quality rules


# Global rule enforcement for item quality boundaries
class ItemQualityRules:
    @staticmethod
    def apply_limits(item):
        if item.name != "Sulfuras, Hand of Ragnaros":
            # Ensure quality is within [0, 50] for all items except Sulfuras
            item.quality = max(0, min(50, item.quality))
        else:
            # Sulfuras always has quality of 80 and never changes
            item.quality = 80


# Abstract base class for item update strategies
class ItemUpdater:
    def __init__(self, item):
        self.item = item

    def update(self):
        raise NotImplementedError  # Must be overridden in subclasses


# Handles generic item update logic
class NormalItemUpdater(ItemUpdater):
    def update(self):
        self._decrease_quality()
        self.item.sell_in -= 1  # Reduce days remaining
        if self.item.sell_in < 0:
            # Degrade quality twice as fast after sell_in date
            self._decrease_quality()

    def _decrease_quality(self, factor=1):
        self.item.quality -= factor


# "Aged Brie" increases in quality the older it gets
class AgedBrieUpdater(ItemUpdater):
    def update(self):
        self._increase_quality()
        self.item.sell_in -= 1
        if self.item.sell_in < 0:
            # Increases quality twice as fast after sell_in date
            self._increase_quality()

    def _increase_quality(self):
        self.item.quality += 1


# "Backstage passes" increase in quality with proximity to sell_in date
class BackstagePassUpdater(ItemUpdater):
    def update(self):
        if self.item.sell_in <= 0:
            # After concert, quality drops to 0
            self.item.quality = 0
        else:
            self._increase_quality()
            if self.item.sell_in <= 10:
                self._increase_quality()
            if self.item.sell_in <= 5:
                self._increase_quality()
        self.item.sell_in -= 1

    def _increase_quality(self):
        self.item.quality += 1


# "Sulfuras" is legendary and does not change
class SulfurasUpdater(ItemUpdater):
    def update(self):
        pass  # No changes for legendary item


# "Conjured" items degrade in quality twice as fast as normal items
class ConjuredItemUpdater(ItemUpdater):
    def update(self):
        self._decrease_quality(2)
        self.item.sell_in -= 1
        if self.item.sell_in < 0:
            # After sell_in, degrade 4 per day
            self._decrease_quality(2)

    def _decrease_quality(self, factor):
        self.item.quality -= factor


# Factory class to return the appropriate updater for a given item
class ItemUpdaterFactory:
    @staticmethod
    def get_updater(item):
        name = item.name
        if name == "Aged Brie":
            return AgedBrieUpdater(item)
        elif name == "Backstage passes to a TAFKAL80ETC concert":
            return BackstagePassUpdater(item)
        elif name == "Sulfuras, Hand of Ragnaros":
            return SulfurasUpdater(item)
        elif name.lower().startswith("conjured"):
            return ConjuredItemUpdater(item)
        else:
            return NormalItemUpdater(item)


# Representation of an item in the system
class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name  # Item name
        self.sell_in = sell_in  # Days remaining to sell
        self.quality = quality  # Current quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
