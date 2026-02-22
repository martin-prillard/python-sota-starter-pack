"""Shared fixtures and utilities for end-to-end tests."""

import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def template_dir():
    """Get the template directory."""
    return Path(__file__).parent.parent.absolute()


@pytest.fixture
def temp_dir():
    """Create a temporary directory for generated projects."""
    temp_path = tempfile.mkdtemp(prefix="cookiecutter-test-")
    yield Path(temp_path)
    # Cleanup
    if Path(temp_path).exists():
        shutil.rmtree(temp_path, ignore_errors=True)


def run_command(cmd: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess:
    """Run a command and return the result."""
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=check,
    )
    # Include both stdout and stderr in error messages for better debugging
    if result.returncode != 0:
        error_msg = f"Command failed: {' '.join(cmd)}\n"
        if result.stderr:
            error_msg += f"STDERR: {result.stderr}\n"
        if result.stdout:
            error_msg += f"STDOUT: {result.stdout}\n"
        result.stderr = error_msg
    return result


def generate_project(
    template_dir: Path,
    output_dir: Path,
    project_type: str,
    project_slug: str = "test-project",
) -> Path:
    """Generate a project using cookiecutter."""
    from cookiecutter.main import cookiecutter

    context = {
        "project_name": "Test Project",
        "project_slug": project_slug,
        "project_description": f"A test {project_type} project",
        "author_name": "Test Author",
        "author_email": "test@example.com",
        "project_type": project_type,
        "python_version": "3.12",
        "use_docker": "yes",
        "publish_to_pypi": "no",
        "pypi_username": "",
        "pypi_token": "",
        "use_ci": "yes",
        "git_provider": "gitlab",
        "gitlab_url": "https://gitlab.com",
        "gitlab_group": "test-group",
        "github_org": "",
        "sonarqube_token": "",
    }

    cookiecutter(
        str(template_dir),
        no_input=True,
        extra_context=context,
        output_dir=str(output_dir),
    )

    project_path = output_dir / project_slug
    assert project_path.exists(), f"Project directory {project_path} was not created"
    
    # Verify essential files exist
    assert (project_path / "pyproject.toml").exists(), f"pyproject.toml not found in {project_path}"
    # Package directory uses underscores (normalized from project_slug)
    package_name = project_slug.replace("-", "_")
    assert (project_path / "src" / package_name).exists(), f"src/{package_name} directory not found"
    
    return project_path


def setup_git_repo(project_path: Path) -> None:
    """Initialize git repository for pre-commit hooks."""
    result = run_command(
        ["git", "init"],
        cwd=project_path,
        check=False,
    )
    # Git init might fail if git is not available, but that's okay for testing
    if result.returncode == 0:
        run_command(
            ["git", "config", "user.email", "test@example.com"],
            cwd=project_path,
            check=False,
        )
        run_command(
            ["git", "config", "user.name", "Test User"],
            cwd=project_path,
            check=False,
        )
        run_command(
            ["git", "add", "."],
            cwd=project_path,
            check=False,
        )


def install_pre_commit(project_path: Path) -> None:
    """Install pre-commit hooks."""
    result = run_command(
        ["uv", "run", "pre-commit", "install"],
        cwd=project_path,
        check=False,
    )
    # Pre-commit install might fail if git is not initialized, that's acceptable for e2e tests
    if result.returncode != 0 and "git" in result.stderr.lower():
        # Skip pre-commit if git is not available
        pass
    else:
        assert result.returncode == 0, f"Failed to install pre-commit hooks: {result.stderr}"
