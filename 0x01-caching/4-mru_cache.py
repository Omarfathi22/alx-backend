#!/usr/bin/env python3
"""Task 4: MRU Caching.
"""
from collections import OrderedDict
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """A class `MRUCache` that inherits from `BaseCaching`.
    This class implements a caching system that uses a 
    Most Recently Used (MRU) eviction policy.
    """

    def __init__(self):
        """Initializes the MRUCache instance and sets up
        the cache data structure as an ordered dictionary.
        """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Adds an item to the cache under the specified key.
        
        If the cache exceeds the maximum allowed items,
        the most recently used item is discarded.
        
        Parameters:
        key (str): The key under which the item will be stored.
        item (Any): The item to be stored in the cache.
        """
        if key is None or item is None:
            return
        
        if key not in self.cache_data:
            if len(self.cache_data) + 1 > BaseCaching.MAX_ITEMS:
                mru_key, _ = self.cache_data.popitem(last=False)
                print("DISCARD:", mru_key)


        self.cache_data[key] = item
        self.cache_data.move_to_end(key, last=False)

    def get(self, key):
        """Retrieves an item from the cache by its key.
        
        If the key exists, it marks the item as recently used.
        
        Parameters:
        key (str): The key of the item to retrieve.
        
        Returns:
        The value associated with the key, or None if the key does not exist.
        """
        if key is not None and key in self.cache_data:

            self.cache_data.move_to_end(key, last=False)
        
        return self.cache_data.get(key, None)
    