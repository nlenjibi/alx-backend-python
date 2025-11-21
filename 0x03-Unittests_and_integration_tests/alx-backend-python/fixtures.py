"""Fixtures for integration tests."""
org_payload = {"login": "google", "url": "https://api.github.com/orgs/google"}
repos_payload = [
    {"name": "repo1", "license": {"key": "apache-2.0"}},
    {"name": "repo2", "license": {"key": "apache-2.0"}},
]
expected_repos = ["repo1", "repo2"]
apache2_repos = ["repo1", "repo2"]
