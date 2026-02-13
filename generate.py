#!/usr/bin/env python3
"""Custom generator script that handles conditional prompts for cookiecutter."""

import json
import os
import subprocess
import sys
from pathlib import Path


def prompt_user(prompt_text: str, default: str = "") -> str:
    """Prompt user for input."""
    if default:
        full_prompt = f"{prompt_text} ({default}): "
    else:
        full_prompt = f"{prompt_text}: "
    
    try:
        response = input(full_prompt).strip()
        return response if response else default
    except (EOFError, KeyboardInterrupt):
        print("\nCancelled.")
        sys.exit(1)


def main() -> None:
    """Main generation function with conditional prompts."""
    print("Python SOTA Starter Pack - Project Generator\n")
    
    # Basic project info
    project_name = prompt_user("project_name", "My Project")
    project_slug = project_name.lower().replace(' ', '-').replace('_', '-')
    project_slug = prompt_user("project_slug", project_slug)
    project_description = prompt_user("project_description", "A modern Python project")
    author_name = prompt_user("author_name", "Your Name")
    author_email = prompt_user("author_email", "your.email@example.com")
    
    # Project type
    print("\nProject types: library, fastapi, streamlit, datascience")
    project_type = prompt_user("project_type", "library")
    
    # Python version
    python_version = prompt_user("python_version", "3.12")
    
    # Docker
    use_docker = prompt_user("use_docker (yes/no)", "yes")
    
    # PyPI publishing
    publish_to_pypi = prompt_user("publish_to_pypi (yes/no)", "no")
    pypi_username = ""
    pypi_token = ""
    if publish_to_pypi.lower() == "yes":
        pypi_username = prompt_user("pypi_username")
        pypi_token = prompt_user("pypi_token")
    
    # CI/CD
    use_ci = prompt_user("use_ci (yes/no)", "yes")
    git_provider = ""
    gitlab_url = ""
    gitlab_group = ""
    github_org = ""
    sonarqube_token = ""
    
    if use_ci.lower() == "yes":
        git_provider = prompt_user("git_provider (gitlab/github)", "gitlab")
        if git_provider.lower() == "gitlab":
            gitlab_url = prompt_user("gitlab_url", "https://gitlab.com")
            gitlab_group = prompt_user("gitlab_group", "your-group")
        elif git_provider.lower() == "github":
            github_org = prompt_user("github_org", "your-org")
        sonarqube_token = prompt_user("sonarqube_token (optional)", "")
    
    # Build context
    context = {
        "project_name": project_name,
        "project_slug": project_slug,
        "project_description": project_description,
        "author_name": author_name,
        "author_email": author_email,
        "project_type": project_type,
        "python_version": python_version,
        "use_docker": use_docker,
        "publish_to_pypi": publish_to_pypi,
        "pypi_username": pypi_username,
        "pypi_token": pypi_token,
        "use_ci": use_ci,
        "git_provider": git_provider,
        "gitlab_url": gitlab_url,
        "gitlab_group": gitlab_group,
        "github_org": github_org,
        "sonarqube_token": sonarqube_token,
    }
    
    # Write context to a temporary JSON file
    template_dir = Path(__file__).parent
    context_file = template_dir / ".cookiecutter_context.json"
    with open(context_file, "w") as f:
        json.dump(context, f)
    
    # Generate project using cookiecutter with no-input mode
    try:
        # Use cookiecutter API directly
        from cookiecutter.main import cookiecutter
        
        cookiecutter(
            str(template_dir),
            no_input=True,
            extra_context=context,
        )
        
        print(f"\n✅ Project generated successfully as {project_type} type!")
        print(f"\nNext steps:")
        print(f"1. cd {project_slug}")
        print(f"2. uv sync")
        print(f"3. uv run pre-commit install")
        print(f"4. Start coding!")
        
    except ImportError:
        print("Error: cookiecutter not installed. Install it with: pip install cookiecutter")
        sys.exit(1)
    except Exception as e:
        print(f"Error generating project: {e}")
        sys.exit(1)
    finally:
        # Clean up context file
        if context_file.exists():
            context_file.unlink()


if __name__ == "__main__":
    main()
