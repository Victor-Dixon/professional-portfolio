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

# Load environment variables
load_dotenv()

class GitHubManager:
    """Secure GitHub repository and profile management tool."""

    def __init__(self):
        self.base_url = "https://api.github.com"
        self.token = self._get_token()
        self.username = self._get_username()
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

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

    def update_repository_descriptions(self, descriptions: Dict[str, str]) -> None:
        """Update repository descriptions for Victor-Dixon repositories."""
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

    def backup_profile_data(self) -> Dict:
        """Backup current profile information."""
        print("
📦 Backing up profile data..."        )

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
        print("
📝 Updating profile README..."        )

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
    parser = argparse.ArgumentParser(description="GitHub Repository & Profile Manager")
    parser.add_argument("--update-descriptions", action="store_true", help="Update repository descriptions")
    parser.add_argument("--backup-profile", action="store_true", help="Backup current profile data")
    parser.add_argument("--update-profile", action="store_true", help="Update profile README")
    parser.add_argument("--list-repos", action="store_true", help="List current repositories")

    args = parser.parse_args()

    if not any([args.update_descriptions, args.backup_profile, args.update_profile, args.list_repos]):
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

        if args.update_profile:
            # Read the README content from the portfolio
            readme_path = Path("README.md")
            if readme_path.exists():
                with open(readme_path, 'r') as f:
                    content = f.read()
                manager.update_profile_readme(content)
            else:
                print("❌ README.md not found in current directory")

    except KeyboardInterrupt:
        print("\n\n👋 Operation cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
