#!/usr/bin/env python3
"""
A module that defines a Server class for paginating data
from a dataset.
"""

from typing import List, Dict, Any, Tuple
import csv
import math


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Retrieves the index range from a given page and page size.

    Args:
        page (int): The page number.
        page_size (int): The number of items per page.

    Returns:
        Tuple[int, int]: A tuple containing the start and end indices.
    """
    start = (page - 1) * page_size
    end = start + page_size
    return (start, end)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initializes a new Server instance.
        """
        self.__dataset = None

    def dataset(self) -> List[List[str]]:
        """Cached dataset

        Returns:
            List[List[str]]: The dataset.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # Skip header

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List[str]]:
        """Retrieves a page of data.

        Args:
            page (int): The page number.
            page_size (int): The number of items per page.

        Returns:
            List[List[str]]: The requested page of the dataset.
        """
        assert isinstance(page, int) and isinstance(page_size, int)
        assert page > 0 and page_size > 0
        start, end = index_range(page, page_size)
        data = self.dataset()
        if start >= len(data):
            return []
        return data[start:end]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Get a hypermedia pagination dictionary.

        Args:
            page (int): The page number.
            page_size (int): The number of items per page.

        Returns:
            Dict[str, Any]: A dictionary with pagination details.
        """
        page_data = self.get_page(page, page_size)
        start, _ = index_range(page, page_size)
        total_pages = math.ceil(len(self.dataset()) / page_size)
        page_info = {
            'page_size': len(page_data),
            'page': page,
            'data': page_data,
            'next_page': page + 1 if start + len(page_data)
            < len(self.dataset()) else None,
            'prev_page': page - 1 if start > 0 else None,
            'total_pages': total_pages,
        }
        return page_info
