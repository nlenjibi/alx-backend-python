#!/usr/bin/env python3
"""Utility functions for unit tests.

Provides: access_nested_map, get_json, memoize
"""
from functools import wraps
import requests


def access_nested_map(nested_map, path):
    """Access a nested map using the sequence of keys in `path`.

    Raises KeyError if a key is missing.
    """
    current = nested_map
    for key in path:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            raise KeyError(key)
    return current


def get_json(url):
    """Get JSON payload from `url` using requests.get()."""
    resp = requests.get(url)
    return resp.json()


def memoize(func):
    """Decorator that caches a method call result as a property on first access.

    Usage:
        @memoize
        def prop(self):
            return expensive()
    """
    attr_name = "_cached_" + func.__name__

    @property
    @wraps(func)
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)

    return wrapper
