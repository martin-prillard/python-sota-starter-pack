"""Pre-generation hook to validate context and set conditional defaults."""

import os
import sys
from pathlib import Path


def main() -> None:
    """Validate context before generation."""
    # This hook runs after prompts but before file generation
    # We can validate and potentially modify the context here
    
    # Get context from environment (CookieCutter sets these)
    context = {}
    for key, value in os.environ.items():
        if key.startswith('COOKIECUTTER_'):
            context[key] = value
    
    # Validate conditional fields
    publish_to_pypi = os.environ.get('COOKIECUTTER_publish_to_pypi', 'no').lower()
    use_ci = os.environ.get('COOKIECUTTER_use_ci', 'yes').lower()
    git_provider = os.environ.get('COOKIECUTTER_git_provider', 'gitlab').lower()
    
    # Set empty defaults for conditional fields if not needed
    if publish_to_pypi != 'yes':
        os.environ['COOKIECUTTER_pypi_username'] = ''
        os.environ['COOKIECUTTER_pypi_token'] = ''
    
    if use_ci != 'yes':
        os.environ['COOKIECUTTER_gitlab_url'] = ''
        os.environ['COOKIECUTTER_gitlab_group'] = ''
        os.environ['COOKIECUTTER_github_org'] = ''
        os.environ['COOKIECUTTER_sonarqube_token'] = ''
    elif git_provider == 'github':
        os.environ['COOKIECUTTER_gitlab_url'] = ''
        os.environ['COOKIECUTTER_gitlab_group'] = ''
    elif git_provider == 'gitlab':
        os.environ['COOKIECUTTER_github_org'] = ''


if __name__ == "__main__":
    main()
