#!/usr/bin/env python3
""" function sum_mixed_list which takes a list mxd_lst of integers and floats
    and returns their sum as a float.
"""
from typing import Union, List


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> Union[int, float]:
    """
    Calculate the sum of a mixed list of integers and floats.

    Args:
        mxd_lst (Union[int, float]): A list containing integers and/or floats.

    Returns:
        Union[int, float]: The sum of the elements in the mixed list.

    Example:
        >>> sum_mixed_list([1, 2, 3.5, 4.2])
        10.7
    """
    return float(sum(mxd_lst))
