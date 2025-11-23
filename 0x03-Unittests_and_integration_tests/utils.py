#!/usr/bin/env python3
"""
Utils module
"""
import requests
from functools import wraps


def access_nested_map(nested_map, path):
    """
    Access nested map with a path
    """
    for key in path:
        if not isinstance(nested_map, dict) or key not in nested_map:
            raise KeyError(key)
        nested_map = nested_map[key]
    return nested_map


def get_json(url):
    """
    Get JSON from URL
    """
    response = requests.get(url)
    return response.json()


def memoize(func):
    """
    Memoize decorator
    """
    cache = {}
    @wraps(func)
    def memoized_func(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return memoized_func