#!/usr/bin/env python3
"""Unit tests for utils module."""
import unittest
from parameterized import parameterized
from unittest.mock import patch

from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test access_nested_map behavior with various inputs."""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        mock_resp = unittest.mock.Mock()
        mock_resp.json.return_value = test_payload
        with patch("requests.get", return_value=mock_resp) as mock_get:
            result = get_json(test_url)
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        obj = TestClass()
        with patch.object(TestClass, 'a_method', return_value=42) as mocked:
            self.assertEqual(obj.a_property, 42)
            self.assertEqual(obj.a_property, 42)
            mocked.assert_called_once()


if __name__ == "__main__":
    unittest.main()
