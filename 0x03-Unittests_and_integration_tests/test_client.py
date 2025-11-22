#!/usr/bin/env python3
"""Tests for the GithubOrgClient class and its integration behavior.

This module contains unit and integration tests for the
`GithubOrgClient` in `client.py`, including fixtures-based integration
tests that simulate requests to the GitHub API.
"""
import os
import sys
import importlib.util
import unittest
from unittest.mock import Mock, patch, PropertyMock

from parameterized import parameterized, parameterized_class

from client import GithubOrgClient

# Load fixtures.py from this directory to avoid import collisions
spec = importlib.util.spec_from_file_location(
    "fixtures",
    os.path.join(os.path.dirname(__file__), "fixtures.py"),
)
fixtures = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixtures)
# Ensure module is importable under the standard name
sys.modules['fixtures'] = fixtures


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for `GithubOrgClient` class (unit level)."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that `org` returns expected payload and calls get_json."""
        mock_get_json.return_value = {"org": org_name}
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, mock_get_json.return_value)
        mock_get_json.assert_called_once_with(
            GithubOrgClient.ORG_URL.format(
                org=org_name
            )
        )

    def test_public_repos_url(self):
        """Test that `_public_repos_url` returns correct repos URL from org."""
        with patch.object(
            GithubOrgClient, 'org', new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/google/repos",
            }
            client = GithubOrgClient('google')
            expected = (
                "https://api.github.com/orgs/google/repos"
            )
            self.assertEqual(client._public_repos_url, expected)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that `public_repos` returns repo names."""
        mocked_payload = [
            {
                "name": "repo1",
                "license": {"key": "apache-2.0"},
            },
            {
                "name": "repo2",
                "license": {"key": "bsd-3-clause"},
            },
        ]
        mock_get_json.return_value = mocked_payload
        with patch.object(
            GithubOrgClient, '_public_repos_url', new_callable=PropertyMock
        ) as mock_pub:
            mock_pub.return_value = (
                "https://api.github.com/orgs/google/repos"
            )
            client = GithubOrgClient('google')
            expected_repos = [
                "repo1",
                "repo2",
            ]
            self.assertEqual(client.public_repos(), expected_repos)
            mock_pub.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        (
            {"license": {"key": "my_license"}},
            "my_license",
            True,
        ),
        (
            {"license": {"key": "other_license"}},
            "my_license",
            False,
        ),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct boolean for repo license keys."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'), [(fixtures.org_payload, fixtures.repos_payload, fixtures.expected_repos, fixtures.apache2_repos),])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient using fixtures."""

    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch('utils.requests.get')
        mock_get = cls.get_patcher.start()
    # make requests.get(...).json() return fixtures based on URL

        # nested function that inspects URL and returns expected fixture
        def _get(url, *args, **kwargs):
            # org URL returns org_payload, repos URL returns repos_payload
            if str(url).endswith('/repos'):
                return Mock(**{"json.return_value": cls.repos_payload})
            return Mock(**{"json.return_value": cls.org_payload})

        mock_get.side_effect = _get

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test: public_repos returns repos from fixtures."""
        client = GithubOrgClient('google')
        self.assertEqual(
            client.public_repos(), self.expected_repos
        )

    def test_public_repos_with_license(self):
        """Integration test: public_repos filtered by license."""
        client = GithubOrgClient('google')
        self.assertEqual(
            client.public_repos('apache-2.0'),
            self.apache2_repos,
        )
