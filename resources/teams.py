import pulumi
import pulumi_github as github

from configs.github_config import GitHubConfig


class GitHubTeams:
    """Manages GitHub teams and memberships."""

    DEFAULT_PRIVACY = "closed"
    DEFAULT_ROLE = "member"

    def __init__(self, config: GitHubConfig):
        self.config = config
        self.teams = {}
        self._create_teams()

    def _create_teams(self) -> None:
        """Create GitHub teams and their memberships based on configuration."""
        for team_name, team_config in self.config.teams.items():
            team = self._create_single_team(team_name, team_config)
            self.teams[team_name] = team
            self._add_team_members(team_name, team)

    def _create_single_team(
        self, team_name: str, team_config: dict
    ) -> github.Team:
        """Create a single GitHub team with specified configuration."""
        return github.Team(
            team_name,
            name=team_name,
            description=team_config.get("description", f"Team {team_name}"),
            privacy=team_config.get("privacy", self.DEFAULT_PRIVACY),
            opts=pulumi.ResourceOptions(protect=False),
        )

    def _add_team_members(self, team_name: str, team: github.Team) -> None:
        """Add members to a specific team."""
        for username in self.config.get_users_for_team(team_name):
            github.Membership(
                f"{team_name}-{username}-membership",
                username=username,
                role=self.DEFAULT_ROLE,
                opts=pulumi.ResourceOptions(depends_on=[team]),
            )