import pulumi
import pulumi_github as github

from configs.github_config import GitHubConfig


class GitHubRepos:
    """Manages GitHub repositories."""

    DEFAULT_VISIBILITY = "private"

    def __init__(self, config: GitHubConfig):
        self.config = config
        self.repos = {}
        self._create_repos()

    def _create_repos(self) -> None:
        """Create GitHub repositories based on configuration."""
        for repo_name, repo_config in self.config.repos.items():
            repo = self._create_single_repo(repo_name, repo_config)
            self.repos[repo_name] = repo

    def _create_single_repo(
        self, repo_name: str, repo_config: dict
    ) -> github.Repository:
        """Create a single GitHub repository with specified configuration."""
        return github.Repository(
            repo_name,
            name=repo_name,
            description=repo_config.get("description", f"Repository {repo_name}"),
            visibility=repo_config.get("visibility", self.DEFAULT_VISIBILITY),
            auto_init=True,
            opts=pulumi.ResourceOptions(protect=False),
        )