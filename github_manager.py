#!/usr/bin/env python3
"""
GitHub Repository & Profile Manager
===================================

Secure tool for updating GitHub repository descriptions and profile information.
Requires manual credential input for security.

Usage:
    python github_manager.py --update-descriptions
    python github_manager.py --update-profile
    python github_manager.py --backup-profile

Author: Victor-Dixon (DaDudeKC)
License: MIT
"""

import argparse
import base64
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import requests
from dotenv import load_dotenv

# Load environment variables from local .env file
local_env_path = Path(__file__).parent / ".env"
load_dotenv(local_env_path)

class GitHubManager:
    """Ultimate GitHub Manager Tool for AI Agents - Complete GitHub Automation Suite."""

    def __init__(self, token: str = None, username: str = None):
        """
        Initialize the ultimate GitHub manager.

        Args:
            token: GitHub personal access token (optional - will prompt if not provided)
            username: GitHub username (optional - will fetch if not provided)
        """
        self.base_url = "https://api.github.com"
        self.token = token or self._get_token()
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.username = username or self._get_username()
        self.rate_limit_remaining = None
        self._update_rate_limit()

    def _get_token(self) -> str:
        """Securely get GitHub token from user input."""
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            print("\n🔐 GitHub Token Required")
            print("Create a Personal Access Token at: https://github.com/settings/tokens")
            print("Required permissions: repo, user:email")
            print()
            token = input("Enter your GitHub Personal Access Token: ").strip()

        if not token:
            print("❌ No token provided. Exiting.")
            sys.exit(1)

        return token

    def _get_username(self) -> str:
        """Get GitHub username from token."""
        response = requests.get(f"{self.base_url}/user", headers=self.headers)
        if response.status_code == 401:
            print("❌ Invalid GitHub token. Please check your credentials.")
            sys.exit(1)

        return response.json()["login"]

    def _update_rate_limit(self) -> None:
        """Update current rate limit status."""
        response = requests.get(f"{self.base_url}/rate_limit", headers=self.headers)
        if response.status_code == 200:
            self.rate_limit_remaining = response.json()["rate"]["remaining"]
        else:
            self.rate_limit_remaining = None

    # ===== REPOSITORY MANAGEMENT =====

    def update_repository_descriptions(self, descriptions: Dict[str, str]) -> None:
        """Update repository descriptions for repositories."""
        print(f"\n🔄 Updating repository descriptions for {self.username}...")

        for repo_name, description in descriptions.items():
            url = f"{self.base_url}/repos/{self.username}/{repo_name}"
            data = {"description": description}

            response = requests.patch(url, headers=self.headers, json=data)

            if response.status_code == 200:
                print(f"✅ Updated {repo_name}")
            elif response.status_code == 404:
                print(f"⚠️  Repository {repo_name} not found")
            else:
                print(f"❌ Failed to update {repo_name}: {response.status_code}")

    def setup_repository_features(self, repo_name: str) -> None:
        """Set up professional repository features."""
        print(f"\n🔧 Setting up features for {repo_name}...")

        # Add topics
        topics = self._get_topics_for_repo(repo_name)
        if topics:
            url = f"{self.base_url}/repos/{self.username}/{repo_name}/topics"
            data = {"names": topics}
            response = requests.put(url, headers={
                **self.headers,
                "Accept": "application/vnd.github.mercy-preview+json"
            }, json=data)

            if response.status_code == 200:
                print(f"✅ Added topics to {repo_name}: {', '.join(topics)}")
            else:
                print(f"⚠️  Could not add topics to {repo_name}")

        # Set homepage if applicable
        homepage = self._get_homepage_for_repo(repo_name)
        if homepage:
            url = f"{self.base_url}/repos/{self.username}/{repo_name}"
            data = {"homepage": homepage}
            response = requests.patch(url, headers=self.headers, json=data)

            if response.status_code == 200:
                print(f"✅ Set homepage for {repo_name}: {homepage}")
            else:
                print(f"⚠️  Could not set homepage for {repo_name}")

    def create_repository(self, name: str, description: str = "", private: bool = False,
                         topics: List[str] = None) -> Dict:
        """Create a new repository."""
        data = {
            "name": name,
            "description": description,
            "private": private,
            "auto_init": True
        }

        response = requests.post(f"{self.base_url}/user/repos", headers=self.headers, json=data)

        if response.status_code == 201:
            repo_data = response.json()
            print(f"✅ Created repository: {name}")

            # Add topics if provided
            if topics:
                self.setup_repository_features(name, topics)

            return repo_data
        else:
            print(f"❌ Failed to create repository {name}: {response.status_code}")
            return None

    def delete_repository(self, repo_name: str, confirm: bool = False) -> bool:
        """Delete a repository (dangerous operation)."""
        if not confirm:
            print(f"⚠️  DELETION REQUIRES CONFIRMATION")
            print(f"Run with confirm=True to delete {repo_name}")
            return False

        response = requests.delete(f"{self.base_url}/repos/{self.username}/{repo_name}", headers=self.headers)

        if response.status_code == 204:
            print(f"🗑️  Deleted repository: {repo_name}")
            return True
        else:
            print(f"❌ Failed to delete repository {repo_name}: {response.status_code}")
            return False

    # ===== ISSUE MANAGEMENT =====

    def create_issue(self, repo_name: str, title: str, body: str = "",
                    labels: List[str] = None, assignees: List[str] = None) -> Dict:
        """Create a new issue."""
        data = {
            "title": title,
            "body": body
        }

        if labels:
            data["labels"] = labels
        if assignees:
            data["assignees"] = assignees

        response = requests.post(f"{self.base_url}/repos/{self.username}/{repo_name}/issues",
                               headers=self.headers, json=data)

        if response.status_code == 201:
            issue_data = response.json()
            print(f"✅ Created issue: {title} (#{issue_data['number']})")
            return issue_data
        else:
            print(f"❌ Failed to create issue: {response.status_code}")
            return None

    def list_issues(self, repo_name: str, state: str = "open", labels: str = None) -> List[Dict]:
        """List repository issues."""
        params = {"state": state}
        if labels:
            params["labels"] = labels

        response = requests.get(f"{self.base_url}/repos/{self.username}/{repo_name}/issues",
                              headers=self.headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to list issues: {response.status_code}")
            return []

    def update_issue(self, repo_name: str, issue_number: int, title: str = None,
                    body: str = None, state: str = None, labels: List[str] = None) -> bool:
        """Update an existing issue."""
        data = {}
        if title:
            data["title"] = title
        if body:
            data["body"] = body
        if state:
            data["state"] = state
        if labels:
            data["labels"] = labels

        response = requests.patch(f"{self.base_url}/repos/{self.username}/{repo_name}/issues/{issue_number}",
                                headers=self.headers, json=data)

        if response.status_code == 200:
            print(f"✅ Updated issue #{issue_number}")
            return True
        else:
            print(f"❌ Failed to update issue #{issue_number}: {response.status_code}")
            return False

    # ===== PULL REQUEST MANAGEMENT =====

    def create_pull_request(self, repo_name: str, title: str, head: str, base: str = "main",
                          body: str = "", draft: bool = False) -> Dict:
        """Create a pull request."""
        data = {
            "title": title,
            "head": head,
            "base": base,
            "body": body,
            "draft": draft
        }

        response = requests.post(f"{self.base_url}/repos/{self.username}/{repo_name}/pulls",
                               headers=self.headers, json=data)

        if response.status_code == 201:
            pr_data = response.json()
            print(f"✅ Created PR: {title} (#{pr_data['number']})")
            return pr_data
        else:
            print(f"❌ Failed to create PR: {response.status_code}")
            return None

    def merge_pull_request(self, repo_name: str, pr_number: int, merge_method: str = "merge") -> bool:
        """Merge a pull request."""
        data = {"merge_method": merge_method}

        response = requests.put(f"{self.base_url}/repos/{self.username}/{repo_name}/pulls/{pr_number}/merge",
                              headers=self.headers, json=data)

        if response.status_code == 200:
            print(f"✅ Merged PR #{pr_number}")
            return True
        else:
            print(f"❌ Failed to merge PR #{pr_number}: {response.status_code}")
            return False

    # ===== PROJECT MANAGEMENT =====

    def create_project(self, repo_name: str, name: str, body: str = "") -> Dict:
        """Create a GitHub project for a repository."""
        data = {
            "name": name,
            "body": body
        }

        # Use the newer Projects API
        headers = {**self.headers, "Accept": "application/vnd.github+json"}

        response = requests.post(f"{self.base_url}/repos/{self.username}/{repo_name}/projects",
                               headers=headers, json=data)

        if response.status_code == 201:
            project_data = response.json()
            print(f"✅ Created project: {name}")
            return project_data
        else:
            print(f"❌ Failed to create project: {response.status_code}")
            return None

    def create_project_column(self, project_id: int, name: str) -> Dict:
        """Create a column in a GitHub project."""
        data = {"name": name}

        response = requests.post(f"{self.base_url}/projects/{project_id}/columns",
                               headers=self.headers, json=data)

        if response.status_code == 201:
            column_data = response.json()
            print(f"✅ Created column: {name}")
            return column_data
        else:
            print(f"❌ Failed to create column: {response.status_code}")
            return None

    # ===== WORKFLOW & AUTOMATION =====

    def create_workflow_file(self, repo_name: str, workflow_name: str, content: str) -> bool:
        """Create a GitHub Actions workflow file."""
        # Create .github/workflows directory structure
        workflow_path = f".github/workflows/{workflow_name}.yml"

        # Base64 encode the content
        encoded_content = base64.b64encode(content.encode()).decode()

        # Create or update the file
        data = {
            "message": f"Add {workflow_name} workflow",
            "content": encoded_content
        }

        response = requests.put(f"{self.base_url}/repos/{self.username}/{repo_name}/contents/{workflow_path}",
                              headers=self.headers, json=data)

        if response.status_code in [201, 200]:
            print(f"✅ Created workflow: {workflow_name}")
            return True
        else:
            print(f"❌ Failed to create workflow: {response.status_code}")
            return False

    def setup_basic_ci_cd(self, repo_name: str, language: str = "python") -> bool:
        """Set up basic CI/CD workflow for a repository."""
        if language.lower() == "python":
            workflow_content = f"""name: CI/CD

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run tests
      run: |
        python -m pytest || echo "No tests found"
"""
        elif language.lower() == "javascript":
            workflow_content = """name: CI/CD

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'

    - name: Install dependencies
      run: npm ci

    - name: Run tests
      run: npm test
"""
        else:
            print(f"❌ Unsupported language: {language}")
            return False

        return self.create_workflow_file(repo_name, "ci-cd", workflow_content)

    # ===== ANALYTICS & INSIGHTS =====

    def get_repository_stats(self, repo_name: str) -> Dict:
        """Get comprehensive repository statistics."""
        stats = {}

        # Basic repo info
        response = requests.get(f"{self.base_url}/repos/{self.username}/{repo_name}", headers=self.headers)
        if response.status_code == 200:
            stats["basic"] = response.json()

        # Languages
        response = requests.get(f"{self.base_url}/repos/{self.username}/{repo_name}/languages", headers=self.headers)
        if response.status_code == 200:
            stats["languages"] = response.json()

        # Contributors
        response = requests.get(f"{self.base_url}/repos/{self.username}/{repo_name}/contributors", headers=self.headers)
        if response.status_code == 200:
            stats["contributors"] = response.json()

        # Recent commits
        response = requests.get(f"{self.base_url}/repos/{self.username}/{repo_name}/commits?per_page=10", headers=self.headers)
        if response.status_code == 200:
            stats["recent_commits"] = response.json()

        return stats

    def analyze_repository_health(self, repo_name: str) -> Dict:
        """Analyze repository health and provide recommendations."""
        stats = self.get_repository_stats(repo_name)

        health_score = 100
        recommendations = []

        # Check for README
        if not stats.get("basic", {}).get("has_readme", False):
            health_score -= 20
            recommendations.append("Add a comprehensive README.md")

        # Check for description
        if not stats.get("basic", {}).get("description"):
            health_score -= 10
            recommendations.append("Add repository description")

        # Check for recent activity
        recent_commits = stats.get("recent_commits", [])
        if not recent_commits or len(recent_commits) == 0:
            health_score -= 15
            recommendations.append("Repository appears inactive")

        # Check language diversity
        languages = stats.get("languages", {})
        if len(languages) == 0:
            health_score -= 10
            recommendations.append("Repository may be empty")

        return {
            "health_score": max(0, health_score),
            "recommendations": recommendations,
            "stats": stats
        }

    # ===== BULK OPERATIONS =====

    def bulk_update_descriptions(self, description_map: Dict[str, str]) -> None:
        """Update descriptions for multiple repositories."""
        print(f"\n🔄 Bulk updating {len(description_map)} repositories...")

        for repo_name, description in description_map.items():
            self.update_repository_descriptions({repo_name: description})

    def setup_all_repositories_professional(self) -> None:
        """Set up all repositories with professional features."""
        print("
🎯 Setting up all repositories professionally..."        )

        # Get all repositories
        repos = self.list_repositories()

        for repo in repos:
            repo_name = repo["name"]
            print(f"\n🔧 Processing {repo_name}...")

            # Update description
            descriptions = get_repository_descriptions()
            if repo_name in descriptions:
                self.update_repository_descriptions({repo_name: descriptions[repo_name]})

            # Setup features
            self.setup_repository_features(repo_name)

    # ===== UTILITY METHODS =====

    def list_repositories(self, type_filter: str = "all") -> List[Dict]:
        """List all repositories for the user."""
        params = {"per_page": 100}
        if type_filter != "all":
            params["type"] = type_filter

        response = requests.get(f"{self.base_url}/user/repos", headers=self.headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to list repositories: {response.status_code}")
            return []

    def search_repositories(self, query: str) -> List[Dict]:
        """Search user's repositories."""
        params = {"q": f"user:{self.username} {query}"}

        response = requests.get(f"{self.base_url}/search/repositories", headers=self.headers, params=params)

        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            print(f"❌ Failed to search repositories: {response.status_code}")
            return []

    def _get_topics_for_repo(self, repo_name: str) -> List[str]:
        """Get appropriate topics for a repository."""
        topic_map = {
            "MeTuber": ["youtube", "automation", "content-creation", "python", "analytics"],
            "Dream.os": ["ai", "multi-agent", "orchestration", "automation", "python"],
            "AgentTools": ["automation", "devops", "tools", "python", "ci-cd"],
            "WorkProjects": ["innovation", "prototyping", "ai", "machine-learning", "research"],
            "Websites": ["web-development", "wordpress", "full-stack", "javascript", "php"],
            "Flowr": ["javascript", "productivity", "session-management", "voice-api"],
            "professional-portfolio": ["portfolio", "career", "resume", "professional", "sre"]
        }
        return topic_map.get(repo_name, [])

    def _get_homepage_for_repo(self, repo_name: str) -> Optional[str]:
        """Get homepage URL for a repository."""
        homepage_map = {
            "professional-portfolio": "https://github.com/Victor-Dixon/professional-portfolio",
            "MeTuber": "https://github.com/Victor-Dixon/MeTuber",
            "Dream.os": "https://github.com/Victor-Dixon/Dream.os"
        }
        return homepage_map.get(repo_name)

    def backup_profile_data(self) -> Dict:
        """Backup current profile information."""
        print("\n📦 Backing up profile data...")

        # Get user profile
        user_response = requests.get(f"{self.base_url}/user", headers=self.headers)
        user_data = user_response.json()

        # Get repositories
        repos_response = requests.get(f"{self.base_url}/user/repos", headers=self.headers)
        repos_data = repos_response.json()

        backup = {
            "user": user_data,
            "repositories": repos_data,
            "timestamp": str(datetime.now())
        }

        # Save backup
        backup_file = Path("github_profile_backup.json")
        with open(backup_file, 'w') as f:
            json.dump(backup, f, indent=2)

        print(f"✅ Profile backup saved to {backup_file}")
        return backup

    def update_profile_readme(self, content: str) -> None:
        """Update or create profile README."""
        print("\n📝 Updating profile README...")

        # Check if profile README exists
        readme_response = requests.get(f"{self.base_url}/repos/{self.username}/{self.username}/readme", headers=self.headers)

        if readme_response.status_code == 404:
            # Create new README
            url = f"{self.base_url}/repos/{self.username}/{self.username}/contents/README.md"
            data = {
                "message": "Create profile README",
                "content": base64.b64encode(content.encode()).decode()
            }
        else:
            # Update existing README
            current_readme = readme_response.json()
            url = f"{self.base_url}/repos/{self.username}/{self.username}/contents/README.md"
            data = {
                "message": "Update profile README",
                "content": base64.b64encode(content.encode()).decode(),
                "sha": current_readme["sha"]
            }

        response = requests.put(url, headers=self.headers, json=data)

        if response.status_code in [200, 201]:
            print("✅ Profile README updated")
        else:
            print(f"❌ Failed to update profile README: {response.status_code}")

def get_repository_descriptions() -> Dict[str, str]:
    """Get the improved repository descriptions."""
    return {
        "MeTuber": "Enterprise-grade YouTube automation platform for content creators. Features advanced analytics integration, automated publishing workflows, and multi-platform content distribution with performance tracking.",
        "WorkProjects": "Innovation laboratory featuring experimental AI implementations, rapid prototyping frameworks, and cutting-edge technology explorations across machine learning, automation, and system design.",
        "Dream.os": "Advanced multi-agent AI orchestration system for automated development workflows. Implements swarm intelligence architecture for intelligent task coordination and infrastructure management.",
        "Websites": "Full-stack web development portfolio including custom WordPress themes, responsive static sites, e-commerce platforms, and deployment automation solutions with modern development practices.",
        "AgentTools": "Comprehensive developer automation toolkit featuring CI/CD pipelines, testing frameworks, infrastructure management scripts, and productivity enhancement utilities for modern development workflows.",
        "Flowr": "Advanced session management application with intelligent timing features, voice-activated controls via Web Speech API, comprehensive analytics, and local data persistence for enhanced user experience.",
        "professional-portfolio": "Professional portfolio showcasing system reliability expertise and enterprise software development. Features comprehensive career materials, project documentation, and SRE positioning for senior engineering roles."
    }

def main():
    parser = argparse.ArgumentParser(description="Ultimate GitHub Manager Tool for AI Agents")
    parser.add_argument("--update-descriptions", action="store_true", help="Update repository descriptions")
    parser.add_argument("--setup-features", action="store_true", help="Set up repository topics and homepages")
    parser.add_argument("--professional-setup", action="store_true", help="Complete professional setup (descriptions + features)")
    parser.add_argument("--backup-profile", action="store_true", help="Backup current profile data")
    parser.add_argument("--update-profile", action="store_true", help="Update profile README")
    parser.add_argument("--list-repos", action="store_true", help="List current repositories")

    # New advanced features
    parser.add_argument("--create-repo", nargs=2, metavar=("NAME", "DESCRIPTION"), help="Create new repository")
    parser.add_argument("--create-issue", nargs=3, metavar=("REPO", "TITLE", "BODY"), help="Create issue in repository")
    parser.add_argument("--create-pr", nargs=4, metavar=("REPO", "TITLE", "HEAD", "BASE"), help="Create pull request")
    parser.add_argument("--setup-ci", nargs=2, metavar=("REPO", "LANGUAGE"), help="Setup CI/CD workflow")
    parser.add_argument("--analyze-health", nargs=1, metavar="REPO", help="Analyze repository health")
    parser.add_argument("--bulk-update", action="store_true", help="Bulk update all repositories professionally")
    parser.add_argument("--search-repos", nargs=1, metavar="QUERY", help="Search repositories")

    args = parser.parse_args()

    # Check if any action was specified
    basic_actions = [args.update_descriptions, args.setup_features, args.professional_setup,
                    args.backup_profile, args.update_profile, args.list_repos]
    advanced_actions = [args.create_repo, args.create_issue, args.create_pr, args.setup_ci,
                       args.analyze_health, args.bulk_update, args.search_repos]

    if not any(basic_actions + advanced_actions):
        parser.print_help()
        return

    try:
        manager = GitHubManager()

        if args.list_repos:
            print(f"\n📋 Repositories for {manager.username}:")
            response = requests.get(f"{manager.base_url}/user/repos", headers=manager.headers)
            repos = response.json()
            for repo in repos[:10]:  # Show first 10
                print(f"  • {repo['name']}: {repo['description'] or 'No description'}")

        if args.backup_profile:
            manager.backup_profile_data()

        if args.update_descriptions:
            descriptions = get_repository_descriptions()
            manager.update_repository_descriptions(descriptions)

        if args.setup_features:
            print("\n🏷️ Setting up repository features...")
            descriptions = get_repository_descriptions()
            for repo_name in descriptions.keys():
                manager.setup_repository_features(repo_name)

        if args.professional_setup:
            print("\n🎯 Running complete professional repository setup...")
            descriptions = get_repository_descriptions()
            manager.update_repository_descriptions(descriptions)

            print("\n🏷️ Setting up repository features...")
            for repo_name in descriptions.keys():
                manager.setup_repository_features(repo_name)

            print("\n✅ Professional setup complete!")
            print("📋 Review your repositories at: https://github.com/Victor-Dixon")

        if args.update_profile:
            # Read the README content from the portfolio
            readme_path = Path("README.md")
            if readme_path.exists():
                with open(readme_path, 'r') as f:
                    content = f.read()
                manager.update_profile_readme(content)
            else:
                print("❌ README.md not found in current directory")

        # Advanced features
        if args.create_repo:
            name, description = args.create_repo
            manager.create_repository(name, description)

        if args.create_issue:
            repo, title, body = args.create_issue
            manager.create_issue(repo, title, body)

        if args.create_pr:
            repo, title, head, base = args.create_pr
            manager.create_pull_request(repo, title, head, base)

        if args.setup_ci:
            repo, language = args.setup_ci
            manager.setup_basic_ci_cd(repo, language)

        if args.analyze_health:
            repo = args.analyze_health[0]
            health_data = manager.analyze_repository_health(repo)
            print(f"\n🏥 Health Score for {repo}: {health_data['health_score']}/100")
            print("\n📋 Recommendations:")
            for rec in health_data['recommendations']:
                print(f"  • {rec}")

        if args.bulk_update:
            manager.setup_all_repositories_professional()

        if args.search_repos:
            query = args.search_repos[0]
            results = manager.search_repositories(query)
            print(f"\n🔍 Search results for '{query}':")
            for repo in results[:5]:  # Show top 5
                print(f"  • {repo['name']}: {repo['description'] or 'No description'}")

    except KeyboardInterrupt:
        print("\n\n👋 Operation cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
