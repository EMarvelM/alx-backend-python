#!/usr/bin/env python3
"""
This module provides a function for creating multiplier functions.

The make_multiplier function returns a function that multiplies a given number by the specified multiplier.

Example:
    >>> multiply_by_2 = make_multiplier(2)
    >>> multiply_by_2(4)
    8
"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """
    Returns a function that multiplies a given number by the specified multiplier.

    Args:
        multiplier (float): The value to multiply the input number by.

    Returns:
        Callable[[float], float]: A function that takes a float as input and returns the result of multiplying it by the multiplier.

    Example:
        >>> multiply_by_2 = make_multiplier(2)
        >>> multiply_by_2(4)
        8
    """
    def custom(x: float) -> float:
        """
        Returns the result of multiplying the input number by the multiplier.

        Args:
            x (float): The number to be multiplied.

        Returns:
            float: The result of multiplying x by the multiplier.
        """
        return multiplier * x

    return custom
