# -*- coding: utf-8 -*-

class GildedRose(object):
    """
    Main system class that processes and updates a list of items.
    """

    def __init__(self, items):
        """
        Initialize with a list of items.
        """
        self.items = items

    def update_quality(self):
        """
        Update quality for each item using the appropriate update strategy,
        and enforce global quality limits.
        """
        for item in self.items:
            updater = ItemUpdaterFactory.get_updater(item)
            updater.update()
            ItemQualityRules.apply_limits(item)


class ItemQualityRules:
    """
    Global rule enforcement for item quality boundaries.
    """

    @staticmethod
    def apply_limits(item):
        """
        Ensure quality stays within [0, 50] for all non-Sulfuras items,
        and exactly 80 for Sulfuras items.
        """
        if not item.name.lower().startswith("sulfuras"):
            item.quality = max(0, min(50, item.quality))
        else:
            item.quality = 80


class ItemUpdater:
    """
    Abstract base class for updating an item.
    Subclasses must implement the 'update' method.
    """

    def __init__(self, item):
        """
        Initialize with the item to be updated.
        """
        self.item = item

    def update(self):
        """
        Update logic for the item. Must be implemented by subclasses.
        """
        raise NotImplementedError


class NormalItemUpdater(ItemUpdater):
    """
    Update strategy for normal items.
    """

    def update(self):
        """
        Decrease sell_in by 1 and degrade quality by 1 (or 2 after sell-in date).
        """
        self.item.sell_in -= 1
        if self.item.sell_in < 0:
            self._decrease_quality(2)
        else:
            self._decrease_quality(1)

    def _decrease_quality(self, factor=1):
        """
        Decrease item quality by a given factor.
        """
        self.item.quality -= factor


class AgedBrieUpdater(ItemUpdater):
    """
    Update strategy for 'Aged Brie', which increases in quality over time.
    """

    def update(self):
        """
        Decrease sell_in by 1 and increase quality (twice as fast after sell-in).
        """
        self.item.sell_in -= 1
        if self.item.sell_in < 0:
            self._increase_quality(2)
        else:
            self._increase_quality(1)

    def _increase_quality(self, factor=1):
        """
        Increase item quality by a given factor.
        """
        self.item.quality += factor


class BackstagePassUpdater(ItemUpdater):
    """
    Update strategy for 'Backstage passes', which increase in quality
    and drop to 0 after the concert.
    """

    def update(self):
        """
        Adjust quality based on proximity to sell-in date.
        """
        self.item.sell_in -= 1
        if self.item.sell_in < 0:
            self.item.quality = 0
        else:
            if self.item.sell_in <= 5:
                self._increase_quality(3)
            elif self.item.sell_in <= 10:
                self._increase_quality(2)
            else:
                self._increase_quality(1)

    def _increase_quality(self, factor=1):
        """
        Increase item quality by a given factor.
        """
        self.item.quality += factor


class SulfurasUpdater(ItemUpdater):
    """
    Update strategy for 'Sulfuras', a legendary item that never changes.
    """

    def update(self):
        """
        Sulfuras does not change; no action needed.
        """
        pass


class ConjuredItemUpdater(ItemUpdater):
    """
    Update strategy for 'Conjured' items, which degrade twice as fast as normal items.
    """

    def update(self):
        """
        Decrease sell_in by 1 and degrade quality faster than normal items.
        """
        self.item.sell_in -= 1
        if self.item.sell_in < 0:
            self._decrease_quality(4)
        else:
            self._decrease_quality(2)

    def _decrease_quality(self, factor):
        """
        Decrease item quality by a given factor.
        """
        self.item.quality -= factor


class ItemUpdaterFactory:
    """
    Factory class to select the appropriate updater for an item.
    """

    @staticmethod
    def get_updater(item):
        """
        Return an appropriate ItemUpdater subclass instance based on item name.
        """
        name = item.name.lower()
        if name.startswith("aged brie"):
            return AgedBrieUpdater(item)
        elif name.startswith("backstage passes"):
            return BackstagePassUpdater(item)
        elif name.startswith("sulfuras"):
            return SulfurasUpdater(item)
        elif name.startswith("conjured"):
            return ConjuredItemUpdater(item)
        else:
            return NormalItemUpdater(item)


class Item:
    """
    Representation of an item in the system.
    """

    def __init__(self, name, sell_in, quality):
        """
        Initialize an item with a name, number of days to sell, and quality.
        """
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        """
        Return a string representation of the item.
        """
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class AddItem:
    """
    Wrapper class to validate and safely add new items.
    """

    def __init__(self, name, sell_in, quality):
        """
        Validate the item attributes and create the item.
        """
        print(f'''Adding item (name: {name}, sell_in: {sell_in}, quality: {quality})''')

        # Validate quality boundaries
        if quality < 0:
            raise ValueError(f"Quality cannot be negative: {quality}")
        if name.lower().startswith("sulfuras") and quality > 80:
            raise ValueError(f"Quality cannot be more than 80 for Sulfuras: {quality}")
        elif not name.lower().startswith("sulfuras") and quality > 50:
            raise ValueError(f"Quality cannot be more than 50 for non-Sulfuras item: {quality}")

        self.item = Item(name, sell_in, quality)

    def __getattr__(self, attr):
        """
        Delegate attribute access to the underlying Item object.
        """
        return getattr(self.item, attr)

    def __repr__(self):
        """
        Return a string representation of the wrapped item.
        """
        return repr(self.item)
