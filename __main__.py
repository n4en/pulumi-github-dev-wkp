import pulumi

from configs.github_config import GitHubConfig
from resources.permissions import GitHubPermissions
from resources.repos import GitHubRepos
from resources.teams import GitHubTeams


def main() -> None:
    """Initialize GitHub resources and export configuration details."""
    config = GitHubConfig()
    teams = GitHubTeams(config)
    repos = GitHubRepos(config)
    permissions = GitHubPermissions(config, teams, repos)

    # Export resource information
    pulumi.export("team_names", list(config.teams.keys()))
    pulumi.export("repo_names", list(config.repos.keys()))


if __name__ == "__main__":
    main()