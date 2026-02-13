"""Post-generation hook to clean up project files based on project type."""

import os
import shutil
from pathlib import Path


def remove_file(filepath: str) -> None:
    """Remove a file if it exists."""
    path = Path(filepath)
    if path.exists():
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)


def main() -> None:
    """Main post-generation cleanup."""
    project_type = "{{ cookiecutter.project_type }}"
    project_root = Path(".")

    # Validate project type
    valid_types = ["library", "fastapi", "streamlit", "datascience"]
    if project_type not in valid_types:
        print(f"⚠️  Warning: Unknown project type '{project_type}'. Valid types: {valid_types}")
        print(f"   Proceeding with '{project_type}' but some features may not work correctly.")

    # Remove test files not relevant to project type
    if project_type == "fastapi":
        remove_file("tests/test_streamlit.py")
        remove_file("tests/test_main.py")
    elif project_type == "streamlit":
        remove_file("tests/test_api.py")
        remove_file("tests/test_main.py")
    elif project_type == "datascience":
        remove_file("tests/test_api.py")
        remove_file("tests/test_streamlit.py")
        # Keep test_main.py for datascience
    else:  # library
        remove_file("tests/test_api.py")
        remove_file("tests/test_streamlit.py")

    # Remove mkdocs for datascience (not typically used)
    if project_type == "datascience":
        remove_file("mkdocs.yml")
        remove_file("docs")

    # Remove notebooks for non-datascience projects
    if project_type != "datascience":
        remove_file("notebooks")

    # Remove Dockerfile if not using Docker
    if "{{ cookiecutter.use_docker }}" != "yes":
        remove_file("Dockerfile")
        remove_file(".dockerignore")

    # Remove CI/CD files based on configuration
    use_ci = "{{ cookiecutter.use_ci }}"
    git_provider = "{{ cookiecutter.git_provider }}"
    
    if use_ci != "yes":
        remove_file(".gitlab-ci.yml")
        remove_file(".github")
        remove_file("sonar-project.properties")
    else:
        # Remove GitLab CI if using GitHub
        if git_provider == "github":
            remove_file(".gitlab-ci.yml")
            remove_file("sonar-project.properties")
        # Remove GitHub workflows if using GitLab
        elif git_provider == "gitlab":
            remove_file(".github")

    # Update .gitlab-ci.yml to remove PyPI publishing if not needed
    if "{{ cookiecutter.publish_to_pypi }}" != "yes" and use_ci == "yes" and git_provider == "gitlab":
        ci_file = project_root / ".gitlab-ci.yml"
        if ci_file.exists():
            content = ci_file.read_text()
            # Remove PyPI publishing sections
            lines = content.split("\n")
            new_lines = []
            skip_section = False
            for line in lines:
                if "build-package:" in line or "publish-pypi:" in line:
                    skip_section = True
                if skip_section and line and not line.startswith(" ") and not line.startswith("\t"):
                    skip_section = False
                if not skip_section:
                    new_lines.append(line)
            ci_file.write_text("\n".join(new_lines))

    print(f"✅ Project generated successfully as {project_type} type!")
    print("\nNext steps:")
    print("1. cd {{ cookiecutter.project_slug }}")
    print("2. uv sync")
    print("3. pre-commit install")
    print("4. Start coding!")


if __name__ == "__main__":
    main()
