#!/usr/bin/env python3
"""Task 0: Basic dictionary
This script defines a simple caching system
using a basic dictionary.
"""

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """A class `BasicCache` that inherits from `BaseCaching`.
    This class implements a basic caching system where
    items can be stored
    and retrieved using keys. It uses a dictionary
    to store the cached data.
    """

    def put(self, key, item):
        """Assigns the value `item` to the dictionary
        `self.cache_data` using the provided `key`.

        Parameters:
        key (str): The key under which the item will be stored.
        item (Any): The value to be stored in the cache.
        """
        
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """Retrieves the value associated with the provided
        `key` from `self.cache_data`.
        """
        return self.cache_data.get(key, None)
    