"""Pre-generation hook to validate context and set conditional defaults."""

import os
import sys
from pathlib import Path


def main() -> None:
    """Validate context before generation."""
    # This hook runs after prompts but before file generation
    # We can validate and potentially modify the context here
    
    # Get user choices
    publish_to_pypi = os.environ.get('COOKIECUTTER_publish_to_pypi', 'no').lower()
    use_ci = os.environ.get('COOKIECUTTER_use_ci', 'yes').lower()
    git_provider = os.environ.get('COOKIECUTTER_git_provider', 'gitlab').lower()
    
    # Clear PyPI fields if not publishing
    if publish_to_pypi != 'yes':
        os.environ['COOKIECUTTER_pypi_username'] = ''
        os.environ['COOKIECUTTER_pypi_token'] = ''
    
    # Handle CI/CD fields based on choices
    if use_ci != 'yes':
        # Clear all CI/CD fields if not using CI
        os.environ['COOKIECUTTER_git_provider'] = ''
        os.environ['COOKIECUTTER_gitlab_url'] = ''
        os.environ['COOKIECUTTER_gitlab_group'] = ''
        os.environ['COOKIECUTTER_github_org'] = ''
        os.environ['COOKIECUTTER_sonarqube_token'] = ''
    else:
        # Clear fields for the non-selected git provider
        if git_provider == 'github':
            # Clear GitLab fields if using GitHub
            os.environ['COOKIECUTTER_gitlab_url'] = ''
            os.environ['COOKIECUTTER_gitlab_group'] = ''
            # Set default for github_org if empty
            if not os.environ.get('COOKIECUTTER_github_org', '').strip():
                os.environ['COOKIECUTTER_github_org'] = 'your-org'
        elif git_provider == 'gitlab':
            # Clear GitHub fields if using GitLab
            os.environ['COOKIECUTTER_github_org'] = ''
            # Set defaults for gitlab fields if empty
            if not os.environ.get('COOKIECUTTER_gitlab_url', '').strip():
                os.environ['COOKIECUTTER_gitlab_url'] = 'https://gitlab.com'
            if not os.environ.get('COOKIECUTTER_gitlab_group', '').strip():
                os.environ['COOKIECUTTER_gitlab_group'] = 'your-group'


if __name__ == "__main__":
    main()
