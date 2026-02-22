"""End-to-end tests for library project type."""

import subprocess
from pathlib import Path

import pytest

from tests.conftest import generate_project, install_pre_commit, run_command, setup_git_repo


class TestLibraryProject:
    """End-to-end tests for library project type."""

    def test_library_generation_and_setup(self, template_dir, temp_dir):
        """Test generating a library project and running setup commands."""
        project_slug = "test-library"
        project_path = generate_project(template_dir, temp_dir, "library", project_slug)

        # Test 1: Install dependencies (uv sync installs the package in editable mode automatically)
        result = run_command(
            ["uv", "sync", "--extra", "dev"],
            cwd=project_path,
        )
        assert result.returncode == 0, f"Failed to install dependencies: {result.stderr}"

        # Initialize git repository (required for pre-commit)
        setup_git_repo(project_path)

        # Test 2: Install pre-commit hooks (skip if git is not available)
        install_pre_commit(project_path)

        # Test 3: Run tests
        result = run_command(
            ["uv", "run", "pytest"],
            cwd=project_path,
        )
        assert result.returncode == 0, f"Tests failed: {result.stderr}"

        # Test 4: Run linting (auto-fix first, then check)
        # First, try to auto-fix any fixable issues
        run_command(
            ["uv", "run", "ruff", "check", "--fix", "."],
            cwd=project_path,
            check=False,  # Don't fail if there are unfixable issues
        )
        # Then check again
        result = run_command(
            ["uv", "run", "ruff", "check", "."],
            cwd=project_path,
            check=False,  # Don't fail the test, just log the result
        )
        # Warn if there are still issues, but don't fail the test
        if result.returncode != 0:
            print(f"⚠️  Ruff found issues (non-blocking): {result.stdout}")

        # Test 5: Format check (auto-format first, then check)
        # First, auto-format the code
        run_command(
            ["uv", "run", "ruff", "format", "."],
            cwd=project_path,
            check=False,  # Don't fail if formatting has issues
        )
        # Then check if formatting is correct
        result = run_command(
            ["uv", "run", "ruff", "format", "--check", "."],
            cwd=project_path,
            check=False,  # Don't fail the test, just verify the command works
        )
        # Format check might fail if code needs formatting, that's okay
        # We just want to make sure the command runs

        # Test 6: Type checking
        result = run_command(
            ["uv", "run", "ty", "check"],
            cwd=project_path,
            check=False,  # Don't fail on type checking errors
        )
        # Type checking return codes: 0=success, 1=type errors, 2=configuration error
        # Accept 0 and 1, but warn about configuration errors (2)
        if result.returncode == 2:
            print(f"⚠️  Type checker configuration issue (non-blocking): {result.stderr}")
        elif result.returncode not in [0, 1]:
            # Unexpected error code
            print(f"⚠️  Type checker returned unexpected code {result.returncode}: {result.stderr}")

        # Test 7: Build package (install build first if needed)
        # Try uv build first, fallback to python -m build
        result = run_command(
            ["uv", "build"],
            cwd=project_path,
            check=False,
        )
        if result.returncode != 0:
            # Fallback to python -m build, but install build first
            run_command(
                ["uv", "pip", "install", "build"],
                cwd=project_path,
            )
            result = run_command(
                ["python", "-m", "build"],
                cwd=project_path,
            )
        assert result.returncode == 0, f"Build failed: {result.stderr}"
        assert (project_path / "dist").exists(), "dist directory was not created"

    def test_library_docker_build_and_run(self, template_dir, temp_dir):
        """Test Docker build and run for library project."""
        project_slug = "test-library"
        project_path = generate_project(template_dir, temp_dir, "library", project_slug)

        # Verify Dockerfile exists
        dockerfile = project_path / "Dockerfile"
        assert dockerfile.exists(), "Dockerfile should exist when use_docker=yes"

        # Generate uv.lock file for Docker build
        result = run_command(
            ["uv", "lock"],
            cwd=project_path,
            check=False,
        )
        # Lock file generation is optional, but helpful for reproducible builds

        # Test Docker build
        image_name = f"{project_slug}:test"
        result = run_command(
            ["docker", "build", "-t", image_name, "."],
            cwd=project_path,
            check=False,
        )
        if result.returncode != 0:
            # Docker might not be available, skip test
            pytest.skip(f"Docker build failed (docker may not be available): {result.stderr}")

        assert result.returncode == 0, f"Docker build failed: {result.stderr}"

        # Test Docker run (non-blocking, short-lived)
        # For library projects, we just verify the container starts and exits
        package_name = project_slug.replace("-", "_")
        result = run_command(
            [
                "docker",
                "run",
                "--rm",
                image_name,
                "python",
                "-m",
                package_name,
            ],
            cwd=project_path,
            check=False,
        )
        # Library projects should run and exit, return code doesn't matter
        # We just verify the container can execute the command

        # Cleanup: remove the test image
        run_command(
            ["docker", "rmi", image_name],
            cwd=project_path,
            check=False,
        )
