# Ultimate GitHub Manager Tool for AI Agents

**Complete GitHub automation suite designed for AI agents and advanced development workflows. Features comprehensive repository management, issue tracking, project automation, and intelligent insights.**

## 🔒 Security First

This tool **never stores your credentials**. You must provide your GitHub Personal Access Token each time you run it.

## 📋 Prerequisites

### 1. Create GitHub Personal Access Token
1. Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Give it a name like "Repository Manager"
4. Select these permissions:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `user:email` (Access user email)
   - ✅ `read:user` (Read user profile data)
5. Copy the token (you'll only see it once!)

### 2. Install Dependencies
```bash
pip install requests python-dotenv
```

## 🚀 Usage

### Core Professional Setup
```bash
python github_manager.py --professional-setup    # Complete professional setup
python github_manager.py --bulk-update          # Bulk update all repositories
python github_manager.py --update-descriptions  # Just descriptions
python github_manager.py --setup-features       # Just topics/homepages
```

### Repository Management
```bash
python github_manager.py --create-repo "repo-name" "description"
python github_manager.py --list-repos
python github_manager.py --search-repos "query"
```

### Issue & PR Management
```bash
python github_manager.py --create-issue "repo" "Issue Title" "Issue body"
python github_manager.py --create-pr "repo" "PR Title" "head-branch" "base-branch"
```

### Automation & CI/CD
```bash
python github_manager.py --setup-ci "repo" "python"  # Python CI/CD
python github_manager.py --setup-ci "repo" "javascript"  # JS CI/CD
```

### Analytics & Insights
```bash
python github_manager.py --analyze-health "repo"    # Health analysis
python github_manager.py --backup-profile          # Profile backup
python github_manager.py --update-profile          # Update profile README
```

### AI Agent Integration
```python
from github_manager import GitHubManager

# Initialize for AI agent use
manager = GitHubManager(token="your_token")

# Automated repository management
manager.setup_all_repositories_professional()

# Health monitoring
health = manager.analyze_repository_health("repo-name")
if health["health_score"] < 70:
    # Auto-create improvement issues
    manager.create_issue("repo-name", "Improve Repository Health",
                        f"Health score: {health['health_score']}\n" +
                        "\n".join(health["recommendations"]))
```

### Backup Your Profile Data
```bash
python github_manager.py --backup-profile
```
Creates `github_profile_backup.json` with your current profile and repository data.

### Update Profile README
```bash
python github_manager.py --update-profile
```
Uses your portfolio README.md as your GitHub profile README.

### List Your Repositories
```bash
python github_manager.py --list-repos
```
Shows current repository names and descriptions.

## 📝 Repository Descriptions Being Applied

| Repository | New Description |
|------------|-----------------|
| **MeTuber** | Enterprise-grade YouTube automation platform for content creators. Features advanced analytics integration, automated publishing workflows, and multi-platform content distribution with performance tracking. |
| **WorkProjects** | Innovation laboratory featuring experimental AI implementations, rapid prototyping frameworks, and cutting-edge technology explorations across machine learning, automation, and system design. |
| **Dream.os** | Advanced multi-agent AI orchestration system for automated development workflows. Implements swarm intelligence architecture for intelligent task coordination and infrastructure management. |
| **Websites** | Full-stack web development portfolio including custom WordPress themes, responsive static sites, e-commerce platforms, and deployment automation solutions with modern development practices. |
| **AgentTools** | Comprehensive developer automation toolkit featuring CI/CD pipelines, testing frameworks, infrastructure management scripts, and productivity enhancement utilities for modern development workflows. |
| **Flowr** | Advanced session management application with intelligent timing features, voice-activated controls via Web Speech API, comprehensive analytics, and local data persistence for enhanced user experience. |
| **professional-portfolio** | Professional portfolio showcasing system reliability expertise and enterprise software development. Features comprehensive career materials, project documentation, and SRE positioning for senior engineering roles. |

## 🔧 Advanced Usage

### Environment Variables (Optional)
Create a `.env` file:
```
GITHUB_TOKEN=your_personal_access_token_here
```

### Custom Descriptions
Edit the `get_repository_descriptions()` function in `github_manager.py` to customize descriptions.

## ⚠️ Security Notes

- **Never commit tokens** to version control
- **Regenerate tokens** if you suspect compromise
- **Use token-specific permissions** (don't give full access)
- **Delete tokens** when no longer needed

## 🐛 Troubleshooting

### "Invalid GitHub token"
- Double-check your token was copied correctly
- Ensure token has required permissions
- Try regenerating the token

### "Repository not found"
- Verify repository name spelling
- Check that you own the repository
- Ensure token has repo permissions

### Rate Limiting
GitHub API has rate limits. The tool shows progress and handles errors gracefully.

## 🎯 Core Features

### 🤖 AI Agent Integration
- **Programmatic API**: Full Python API for AI agent integration
- **Batch Operations**: Bulk repository management and updates
- **Automated Workflows**: CI/CD setup, issue management, health monitoring
- **Intelligent Insights**: Repository analysis and recommendations

### 📊 Repository Management
- **Professional Setup**: Complete repository professionalization
- **Health Analysis**: Comprehensive repository health scoring
- **Bulk Operations**: Update multiple repositories simultaneously
- **Search & Discovery**: Advanced repository search capabilities

### 🔄 Issue & Project Automation
- **Issue Management**: Create, update, and track issues programmatically
- **Pull Request Handling**: Automated PR creation and merging
- **Project Boards**: GitHub Projects creation and management
- **Workflow Automation**: GitHub Actions setup and management

### 📈 Analytics & Insights
- **Repository Health**: Comprehensive health scoring and recommendations
- **Activity Monitoring**: Commit patterns, contributor analysis, language stats
- **Performance Metrics**: Repository performance and optimization insights
- **Trend Analysis**: Repository growth and engagement tracking

### 🛠️ Development Automation
- **CI/CD Setup**: Automated workflow creation for multiple languages
- **Quality Assurance**: Automated testing and linting setup
- **Dependency Management**: Automated dependency updates and security checks
- **Branch Protection**: Automated branch protection rule setup

## 📊 What Gets Updated

### Repository Settings
- ✅ Description field with professional copy
- ✅ Topics/tags for discoverability (youtube, automation, ai, devops, etc.)
- ✅ Homepage URL linking to documentation
- ✅ Professional categorization and organization

### Profile Settings
- ✅ Profile README with portfolio integration
- ✅ Profile backup and restoration
- ✅ Activity analytics and insights

### Automation Features
- ✅ CI/CD workflows (Python, JavaScript, etc.)
- ✅ Issue templates and project boards
- ✅ Branch protection and code quality rules
- ✅ Automated health monitoring and alerts

## 🔄 Repository Migration Workflow

### Phase 1: Complete Master Tasks (Current)
- ✅ Complete all tasks in `UNIFIED_MASTER_TASK_LIST.md`
- ✅ Ensure all repositories meet quality standards
- ✅ Test and validate all functionality

### Phase 2: Professional Setup (Using This Tool)
```bash
# After completing all master tasks:
python github_manager.py --professional-setup
```

### Phase 3: Repository Organization (Future)
- Move repositories to appropriate categories
- Set up GitHub Projects for kanban tracking
- Configure repository visibility and access
- Update all cross-repository references

### Phase 4: Profile Migration (If Needed)
- Transfer repositories to new GitHub account
- Update all documentation links
- Reconfigure CI/CD pipelines
- Update portfolio with new repository URLs

## 🔄 Integration with Kanban

Use this tool as part of your kanban workflow:
1. Complete repository improvement tasks in kanban
2. Run `python github_manager.py --update-descriptions`
3. Move tasks to "Done" column

## 🎯 Quick Start

```bash
# 1. Get your GitHub token
# 2. Install dependencies: pip install requests python-dotenv
# 3. Run: python github_manager.py --update-descriptions
# 4. Verify changes on github.com/Victor-Dixon
```

**Tool available at:** [github.com/Victor-Dixon/professional-portfolio/github_manager.py](https://github.com/Victor-Dixon/professional-portfolio/blob/main/github_manager.py)
