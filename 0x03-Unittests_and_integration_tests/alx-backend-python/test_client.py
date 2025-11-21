#!/usr/bin/env python3
"""Unit and integration tests for client module."""
import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, Mock

from client import GithubOrgClient
import fixtures


class TestGithubOrgClient(unittest.TestCase):
	@parameterized.expand(["google", "abc"])
	@patch("client.get_json")
	def test_org(self, org_name, mock_get_json):
		mock_get_json.return_value = {"login": org_name}
		client = GithubOrgClient(org_name)
		self.assertEqual(client.org(), {"login": org_name})
		expected_url = (
			f"https://api.github.com/orgs/{org_name}"
		)
		mock_get_json.assert_called_once_with(expected_url)

	def test_public_repos_url(self):
		client = GithubOrgClient('google')
		payload = {
			"repos_url": "https://api.github.com/orgs/google/repos"
		}
		with patch.object(GithubOrgClient, 'org', return_value=payload):
			self.assertEqual(client._public_repos_url, payload['repos_url'])

	@patch("client.get_json")
	def test_public_repos(self, mock_get_json):
		test_payload = [{"name": "repo1"}, {"name": "repo2"}]
		mock_get_json.return_value = test_payload
		client = GithubOrgClient('org')
		with patch.object(
			GithubOrgClient, '_public_repos_url', return_value='https://api'
		):
			repos = client.public_repos()
			self.assertEqual(repos, ["repo1", "repo2"])
		mock_get_json.assert_called_once()

	@parameterized.expand([
		({"license": {"key": "my_license"}}, "my_license", True),
		({"license": {"key": "other_license"}}, "my_license", False),
	])
	def test_has_license(self, repo, license_key, expected):
		client = GithubOrgClient('org')
		self.assertEqual(client.has_license(repo, license_key), expected)


@parameterized_class(('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'), [
	(fixtures.org_payload, fixtures.repos_payload, fixtures.expected_repos, fixtures.apache2_repos),
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.get_patcher = patch('requests.get')
		mocked_get = cls.get_patcher.start()

		# Setup side effects for requests.get().json()
		def _json_side_effect(url, *args, **kwargs):
			mock = Mock()
			if url.endswith('/orgs/google'):
				mock.json.return_value = fixtures.org_payload
			else:
				mock.json.return_value = fixtures.repos_payload
			return mock

		mocked_get.side_effect = _json_side_effect

	@classmethod
	def tearDownClass(cls):
		cls.get_patcher.stop()

	def test_public_repos_integration(self):
		client = GithubOrgClient('google')
		repos = client.public_repos()
		self.assertEqual(repos, self.expected_repos)


if __name__ == '__main__':
	unittest.main()
