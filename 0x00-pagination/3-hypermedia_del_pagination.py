#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict, Any, Tuple

def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Retrieves the index range from a given page and page size.

    Args:
        page (int): The page number.
        page_size (int): The number of items per page.

    Returns:
        Tuple[int, int]: A tuple containing the start and end indices.
    """
    return ((page - 1) * page_size, (page - 1) * page_size + page_size)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List[str]]:
        """Cached dataset.

        Returns:
            List[List[str]]: The dataset.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # Skip header

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List[str]]:
        """Dataset indexed by sorting position, starting at 0.

        Returns:
            Dict[int, List[str]]: The indexed dataset.
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {i: dataset[i] for i in range(len(dataset))}
        return self.__indexed_dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List[str]]:
        """Retrieves a page of data.

        Args:
            page (int): The page number.
            page_size (int): The number of items per page.

        Returns:
            List[List[str]]: The requested page of the dataset.
        """
        assert type(page) == int and type(page_size) == int
        assert page > 0 and page_size > 0
        start, end = index_range(page, page_size)
        data = self.dataset()
        if start >= len(data):
            return []
        return data[start:end]

    def get_hyper_index(self, index: int = 0, page_size: int = 10) -> Dict[str, Any]:
        """Retrieves a page of data with deletion-resilience.

        Args:
            index (int): The starting index for the page.
            page_size (int): The number of items to return.

        Returns:
            Dict[str, Any]: A dictionary containing pagination information.
        """
        assert index is not None and index >= 0
        indexed_data = self.indexed_dataset()
        
        page_data = []
        next_index = index
        data_count = 0
        
        while data_count < page_size:
            if next_index in indexed_data:
                page_data.append(indexed_data[next_index])
                data_count += 1
            next_index += 1
        
        return {
            'index': index,
            'next_index': next_index,
            'page_size': len(page_data),
            'data': page_data,
        }
