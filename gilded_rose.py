# -*- coding: utf-8 -*-

class GildedRose(object):
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            updater = ItemUpdaterFactory.get_updater(item)
            updater.update()
            ItemQualityRules.apply_limits(item)  # ✅ Enforce constraints globally


# Common rule enforcement class
class ItemQualityRules:
    @staticmethod
    def apply_limits(item):
        if item.name != "Sulfuras, Hand of Ragnaros":
            item.quality = max(0, min(50, item.quality))
        else:
            item.quality = 80  # Legendary quality is always 80


# Strategy classes
class ItemUpdater:
    def __init__(self, item):
        self.item = item

    def update(self):
        raise NotImplementedError


class NormalItemUpdater(ItemUpdater):
    def update(self):
        self._decrease_quality()
        self.item.sell_in -= 1
        if self.item.sell_in < 0:
            self._decrease_quality()

    def _decrease_quality(self, factor=1):
        self.item.quality -= factor


class AgedBrieUpdater(ItemUpdater):
    def update(self):
        self._increase_quality()
        self.item.sell_in -= 1
        if self.item.sell_in < 0:
            self._increase_quality()

    def _increase_quality(self):
        self.item.quality += 1


class BackstagePassUpdater(ItemUpdater):
    def update(self):
        if self.item.sell_in <= 0:
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


class SulfurasUpdater(ItemUpdater):
    def update(self):
        # Legendary item: no update required
        pass


class ConjuredItemUpdater(ItemUpdater):
    def update(self):
        self._decrease_quality(2)
        self.item.sell_in -= 1
        if self.item.sell_in < 0:
            self._decrease_quality(2)

    def _decrease_quality(self, factor):
        self.item.quality -= factor


# Factory pattern
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


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
