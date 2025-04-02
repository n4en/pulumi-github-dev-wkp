import pulumi
import pulumi_github as github

from configs.github_config import GitHubConfig
from resources.repos import GitHubRepos
from resources.teams import GitHubTeams


class GitHubPermissions:
    """Manages GitHub team permissions for repositories."""

    VALID_PERMISSIONS = {"pull", "push", "admin", "maintain", "triage"}

    def __init__(self, config: GitHubConfig, teams: GitHubTeams, repos: GitHubRepos):
        self.config = config
        self.teams = teams
        self.repos = repos
        self._assign_permissions()

    def _assign_permissions(self) -> None:
        """Assign team permissions to repositories based on configuration."""
        for repo_name, repo_config in self.config.repos.items():
            repo = self.repos.repos.get(repo_name)
            if repo:
                self._assign_team_permissions(repo_name, repo, repo_config)

    def _assign_team_permissions(
        self, repo_name: str, repo: github.Repository, repo_config: dict
    ) -> None:
        """Assign permissions for all teams to a specific repository."""
        team_permissions = repo_config.get("permissions", {})
        for team_name, permissions in team_permissions.items():
            team = self.teams.teams.get(team_name)
            if team:
                self._create_team_repository_permissions(team, repo, repo_name, permissions)

    def _create_team_repository_permissions(
        self,
        team: github.Team,
        repo: github.Repository,
        repo_name: str,
        permissions: list,
    ) -> None:
        """Create team repository permission resources for valid permissions."""
        def create_permission(team_id: str, permission: str) -> None:
            github.TeamRepository(
                f"{team_id}-{repo_name}-{permission}-permission",
                team_id=team_id,
                repository=repo_name,
                permission=permission,
                opts=pulumi.ResourceOptions(depends_on=[team, repo]),
            )

        for permission in permissions:
            if permission in self.VALID_PERMISSIONS:
                team.id.apply(lambda team_id: create_permission(team_id, permission))