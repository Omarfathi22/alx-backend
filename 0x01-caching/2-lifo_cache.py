#!/usr/bin/env python3
"""Task 2: LIFO caching.
"""
from collections import OrderedDict
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """Represents a caching system that stores items
    in a dictionary with a Last In, First Out (LIFO)
    removal mechanism when the cache limit is reached.
    """
    
    def __init__(self):
        """Initializes the LIFOCache instance, setting up
        the cache data structure as an ordered dictionary.
        """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Adds an item to the cache with the specified key.
        
        If the cache exceeds the maximum allowed items,
        the least recently added item is discarded (LIFO).
        
        Parameters:
        key (str): The key under which the item will be stored.
        item (Any): The item to be stored in the cache.
        """
        if key is None or item is None:
            return
        
        if key not in self.cache_data:
            if len(self.cache_data) + 1 > BaseCaching.MAX_ITEMS:
                last_key, _ = self.cache_data.popitem(True)
                print("DISCARD:", last_key)
        
        self.cache_data[key] = item
        self.cache_data.move_to_end(key, last=True)

    def get(self, key):
        """Retrieves an item from the cache by its key.
        
        Returns:
        The value associated with the key, or None if the key does not exist.
        """
        return self.cache_data.get(key, None)
    