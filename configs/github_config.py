import os
from typing import Dict, List, Optional

import pulumi
import yaml


class GitHubConfig:
    """Configuration manager for GitHub."""

    CONFIG_DIR = os.path.dirname(__file__)
    DEFAULT_EMPTY_DICT = {}

    def __init__(self):
        self.config = pulumi.Config()
        self.teams = self._load_yaml("teams.yaml")
        self.repos = self._load_yaml("repos.yaml")
        self.user_team_mappings = self._load_yaml("user_team_mappings.yaml")

    def _load_yaml(self, filename: str) -> Dict:
        """Load YAML file from config directory and return its contents."""
        file_path = os.path.join(self.CONFIG_DIR, filename)
        try:
            with open(file_path, "r") as file:
                return yaml.safe_load(file) or self.DEFAULT_EMPTY_DICT
        except FileNotFoundError:
            return self.DEFAULT_EMPTY_DICT

    def get_team_config(self, team_name: str) -> Optional[Dict]:
        """Get configuration for a specific team."""
        return self.teams.get(team_name)

    def get_repo_config(self, repo_name: str) -> Optional[Dict]:
        """Get configuration for a specific repository."""
        return self.repos.get(repo_name)

    def get_users_for_team(self, team_name: str) -> List[str]:
        """Get list of users for a specific team."""
        return self.user_team_mappings.get(team_name, [])

    def get_team_permissions_for_repo(self, repo_name: str) -> Dict[str, str]:
        """Get team permissions for a specific repository."""
        return self.get_repo_config(repo_name).get("team_permissions", {})