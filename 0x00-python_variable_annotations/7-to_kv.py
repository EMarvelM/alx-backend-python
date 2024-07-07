#!/usr/bin/env python3
""" This module contains a function to_kv that takes a string and a number as
    input and returns a tuple containing the string and square of the number.
"""


def to_kv(k: str, v: int | float) -> tuple:
    """
    Takes a string and a number as input and returns a tuple containing
    the string and the square of the number.

    Args:
        k (str): The input string.
        v (int | float): The input number.

    Returns:
        tuple: A tuple containing the string and the square of the number.
    """
    return (k, float(v * v))