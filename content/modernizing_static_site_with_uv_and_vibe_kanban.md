Title: Modernizing a Static Site with UV and Vibe-Kanban: A Developer's Journey
Date: 2025-01-27
Category: Development
Tags: python, uv, pelican, static-site, vibe-kanban, modernization
Slug: modernizing-static-site-with-uv-and-vibe-kanban
Summary: How I used Vibe-Kanban to upgrade my static site from traditional pip to modern UV package management while making the code more pythonic.

# Introduction

Recently, I discovered [Vibe-Kanban](https://www.vibekanban.com/), a fascinating approach to task management that leverages AI assistance for project development. Today, I'll share how I used it to modernize my Pelican-based static website, transitioning from traditional Python package management to the modern UV tool while making the codebase more pythonic.

In my daily work - I already use code assistance in many ways - mainly by giving context (building an outline of the tasks in a markdown document), and then executy the tasks (mainly using Claude and [Aider](https://aider.chat/)). 

Working with the Vibe-Kanban was a very pleasant experience, here is what i was able to accomplish in aprox. 15 min (including this blog post). 

## What is Vibe-Kanban?

Vibe-Kanban is an AI-powered development workflow that combines task management with intelligent code assistance. It helps break down complex projects into manageable tasks while providing context-aware development support. The key benefit is having an AI assistant that understands your project structure and can execute multi-step tasks autonomously.

## The Challenge: Legacy Python Project Setup

My static site was running on a typical legacy Python setup:  
- `requirements.txt` for dependencies  
- Python 3.12 (causing compatibility issues)  
- Old-style string formatting and code patterns  
- Manual dependency management  

The goal was to modernize this setup using UV, Python's fastest package manager, while improving code quality.

## Basic Steps to Use Vibe-Kanban

Here's how to get started with Vibe-Kanban for your own projects:

### 1. Set Up the Environment
```bash
# Clone or access your project
cd your-project

# Ensure you have Claude Code CLI available
# Follow the setup instructions at https://docs.anthropic.com/claude-code
```

### 2. Define Your Upgrade Task
Instead of manually planning every step, you provide a high-level description:

```
Task title: upgrade static site
Task description: Using UV update the project to be pythonic and updated.
create a new branch before making any changes
```

### 3. Let the AI Assistant Plan and Execute
The AI breaks down your task into manageable todos:   
- Create new branch for upgrade.  
- Analyze current project structure.   
- Review existing dependencies and configuration.  
- Migrate to uv package management.  
- Update Python code to be more pythonic.  
- Test the upgraded project.  

### 4. Monitor Progress
The AI provides real-time updates on task completion, ensuring nothing is missed.

### 5. Iterate  
Add additional instructions as part of the review and let the agent run.

## The Modernization Process

Here's what the AI accomplished during my website upgrade:

### Branch Creation and Analysis
First, it created a new branch `upgrade-to-uv-pythonic` and analyzed the existing project structure, identifying:
- Python files that needed updating
- Dependency management files
- Configuration files requiring modernization

### UV Migration
The most significant change was migrating from `requirements.txt` to a modern `pyproject.toml`:

```toml
[project]
name = "sephib-github-io"
version = "0.1.0"
description = "Static site generator for Sephi's blog using Pelican"
requires-python = ">=3.10,<3.12"
dependencies = [
    "pelican<=4.9.1",
    "pelican-jupyter>=0.10.1",
    ...
]

[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
    "ruff>=0.1.0",
]
```

### Code Modernization
The AI systematically updated the codebase to be more pythonic, for example:

**Before:**
```python
"commit_message": "'Publish site on {}'".format(datetime.date.today().isoformat()),
```

**After:**
```python
"commit_message": f"'Publish site on {datetime.date.today().isoformat()}'",
```

**Before:**
```python
if os.path.isdir(CONFIG["deploy_path"]):
    shutil.rmtree(CONFIG["deploy_path"])
    os.makedirs(CONFIG["deploy_path"])
```

**After:**
```python
deploy_path = Path(CONFIG["deploy_path"])
if deploy_path.exists():
    shutil.rmtree(deploy_path)
    deploy_path.mkdir(parents=True, exist_ok=True)
```

### Dependency Resolution
One of the trickiest parts was resolving version conflicts between packages. The AI:  
- Identified compatibility issues between Jinja2, Pelican, and nbconvert   
- Adjusted Python version requirements from 3.12 to 3.10-3.11   
- Fixed plugin configurations that were causing build failures   

### Testing and Validation
Finally, the AI tested the entire setup:
```bash
uv sync --python 3.11 --index-strategy unsafe-best-match
uv run invoke build
uv run invoke serve
```

## Key Benefits of This Approach

### 1. **Systematic Task Management**
Instead of ad-hoc changes, every modification was tracked and purposeful.

### 2. **Modern Tooling**
- UV provides faster dependency resolution  
- Better dependency locking with `uv.lock`  
- Improved virtual environment management  

### 3. **Code Quality Improvements**
- F-strings for better performance and readability  
- Pathlib for modern file operations  
- Proper import ordering  
- Removed unused imports  

### 4. **Version Compatibility**
The AI automatically resolved complex version conflicts that would have taken hours to debug manually.

## Running the Development Server

With the modernized setup, running the development server is straightforward:

```bash
# Build and serve the site
uv run invoke reserve

# Or for live reload during development
uv run invoke livereload

# Just build
uv run invoke build
```

The site now serves at `http://localhost:8000` with automatic rebuilding capabilities.

## Lessons Learned

### 1. **AI-Assisted Development is Powerful**
Having an AI that understands project context and can execute multi-step tasks is incredibly valuable for modernization projects.

### 2. **Systematic Approaches Work**
Breaking down complex upgrades into discrete, trackable tasks prevents mistakes and ensures completeness.


## Future Improvements

With this foundation in place, future enhancements could include:  
- Implementing automated testing for content. 
- Adding GitHub Actions for deployment. 
- Exploring newer Pelican themes. 
- Adding MCP servers

## Conclusion

Vibe-Kanban transformed what could have been a tedious, error-prone modernization process into a systematic, well-documented upgrade. The combination of AI assistance and modern Python tooling like UV creates a powerful development workflow.

The key is providing clear goals and letting the AI handle the detailed implementation while maintaining oversight of the process. This approach scales well for any Python project modernization effort.

