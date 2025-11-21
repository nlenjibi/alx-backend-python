#!/usr/bin/env python3
"""Client module for interacting with the GitHub API used in tests."""
from typing import List

import requests
from utils import get_json


class GithubOrgClient:
    """Simple client for GitHub organization endpoints."""

    def __init__(self, org_name: str) -> None:
        self.org_name = org_name

    def org(self):
        """Return the organisation payload from the GitHub API."""
        return get_json(f"https://api.github.com/orgs/{self.org_name}")

    @property
    def _public_repos_url(self) -> str:
        """Return the URL for the organization's public repos."""
        return self.org().get("repos_url")

    def public_repos(self, license: str = None) -> List[str]:
        """Return a list with the repository names for the organization.

        If `license` is provided, only repos that match the license key
        are returned.
        """
        repos = get_json(self._public_repos_url)
        repo_names = []
        for repo in repos:
            if license is None or self.has_license(repo, license):
                repo_names.append(repo.get("name"))
        return repo_names

    @staticmethod
    def has_license(repo: dict, license_key: str) -> bool:
        """Return True if `repo` contains a license with `license_key`."""
        lic = repo.get("license") or {}
        return lic.get("key") == license_key
