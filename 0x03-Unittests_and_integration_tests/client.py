#!/usr/bin/env python3
"""
Client module
"""
from utils import get_json, memoize


class GithubOrgClient:
    """
    Github Org Client
    """
    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name):
        self._org_name = org_name

    @memoize
    def org(self):
        """
        Get org data
        """
        return get_json(self.ORG_URL.format(org=self._org_name))

    @property
    def _public_repos_url(self):
        """
        Public repos URL
        """
        return self.org.get("repos_url")

    @memoize
    def public_repos(self):
        """
        Public repos
        """
        repos_url = self._public_repos_url
        if repos_url:
            repos = get_json(repos_url)
            return [repo.get("name") for repo in repos]
        return []

    @staticmethod
    def has_license(repo, license_key):
        """
        Check if repo has license
        """
        licenses = repo.get("license")
        if licenses and licenses.get("key") == license_key:
            return True
        return False