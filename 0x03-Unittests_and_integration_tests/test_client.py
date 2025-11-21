from unittest import TestCase
from unittest.mock import patch, Mock
from parameterized import parameterized_class

from client import GithubOrgClient
import fixtures


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [
        (
            fixtures.org_payload,
            fixtures.repos_payload,
            fixtures.expected_repos,
            fixtures.apache2_repos,
        )
    ],
)
class TestIntegrationGithubOrgClient(TestCase):
    """Integration tests for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get and set side_effect to return fixtures."""

        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            mock_response = Mock()

            if url == "https://api.github.com/orgs/google":
                mock_response.json.return_value = cls.org_payload

            elif url == "https://api.github.com/orgs/google/repos":
                mock_response.json.return_value = cls.repos_payload

            return mock_response

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos without license filter."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos with license filter."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )
