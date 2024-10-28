#!/usr/bin/env python3
"""
This module contains a helper function for pagination.
"""

from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Retrieves the index range from a given page and page size.
    Returns a tuple of size two containing a start index and an end index
    corresponding to the range of indexes to return in a list for those 
    particular pagination parameters
    """
    start = (page - 1) * page_size
    end = start + page_size
    return (start, end)
