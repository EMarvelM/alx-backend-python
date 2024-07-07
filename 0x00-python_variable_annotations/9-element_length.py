#!/usr/bin/env python3
"""
Module to calculate the length of elements in an iterable.
"""
from typing import Iterable, Sequence, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """
    Calculate the length of each element in the given iterable.

    Args:
        lst: An iterable containing sequences.

    Returns:
        A list of tuples, where each tuple contains a sequence from the input
        iterable and its corresponding length.

    Example:
        >>> element_length(['apple', 'banana', 'cherry'])
        [('apple', 5), ('banana', 6), ('cherry', 6)]
    """
    return [(i, len(i)) for i in lst]
