#!/usr/bin/env python3
"""Fixtures for tests
"""
org_payload = {"repos_url": "https://api.github.com/orgs/google/repos"}

repos_payload = [
    {"name": "repo1", "license": {"key": "apache-2.0"}},
    {"name": "repo2", "license": {"key": "bsd-3-clause"}},
    {"name": "repo3", "license": {"key": "apache-2.0"}},
]

expected_repos = [r["name"] for r in repos_payload]

apache2_repos = [r["name"] for r in repos_payload if r["license"]["key"] == "apache-2.0"]
