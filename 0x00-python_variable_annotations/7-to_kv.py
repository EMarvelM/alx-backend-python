"""  
This module contains a function to_kv that takes a string and a number as input and returns a tuple containing the string and the square of the number.

Example:
    to_kv("x", 3) returns ("x", 9.0)
"""

def to_kv(k: str, v: int | float) -> tuple:
    """
    Takes a string and a number as input and returns a tuple containing the string and the square of the number.

    Args:
        k (str): The input string.
        v (int | float): The input number.

    Returns:
        tuple: A tuple containing the string and the square of the number.
    """
    return (k, float(v * v))
