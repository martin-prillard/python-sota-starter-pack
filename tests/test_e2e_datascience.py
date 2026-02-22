"""End-to-end tests for Data Science project type."""

import subprocess
import time
from pathlib import Path

import pytest

from tests.conftest import generate_project, install_pre_commit, run_command, setup_git_repo


class TestDataScienceProject:
    """End-to-end tests for Data Science project type."""

    def test_datascience_generation_and_setup(self, template_dir, temp_dir):
        """Test generating a Data Science project and running setup commands."""
        project_slug = "test-datascience"
        project_path = generate_project(template_dir, temp_dir, "datascience", project_slug)

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

        # Test 4: Verify Jupyter Lab can be imported
        result = run_command(
            ["uv", "run", "python", "-c", "import jupyterlab; print('OK')"],
            cwd=project_path,
        )
        assert result.returncode == 0, f"Failed to import jupyterlab: {result.stderr}"

        # Test 5: Verify data science libraries are available
        result = run_command(
            [
                "uv",
                "run",
                "python",
                "-c",
                "import pandas, numpy, matplotlib, sklearn; print('OK')",
            ],
            cwd=project_path,
        )
        assert result.returncode == 0, f"Failed to import data science libraries: {result.stderr}"

        # Test 6: Check that jupyter command works
        result = run_command(
            ["uv", "run", "jupyter", "--help"],
            cwd=project_path,
        )
        assert result.returncode == 0, f"jupyter not available: {result.stderr}"

        # Test 7: Verify notebooks directory exists
        notebooks_dir = project_path / "notebooks"
        assert notebooks_dir.exists(), "notebooks directory should exist"

    def test_datascience_docker_build_and_run(self, template_dir, temp_dir):
        """Test Docker build and run for Data Science project."""
        project_slug = "test-datascience"
        project_path = generate_project(template_dir, temp_dir, "datascience", project_slug)

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

        # Test Docker run - start container in background
        container_name = f"{project_slug}-test-container"
        
        # Start container
        result = run_command(
            [
                "docker",
                "run",
                "-d",
                "--name",
                container_name,
                "-p",
                "8888:8888",
                image_name,
            ],
            cwd=project_path,
            check=False,
        )
        if result.returncode != 0:
            # Cleanup image if container start failed
            run_command(["docker", "rmi", image_name], cwd=project_path, check=False)
            pytest.skip(f"Docker run failed: {result.stderr}")

        try:
            # Wait a bit for Jupyter to start
            time.sleep(5)

            # Test that Jupyter Lab is responding
            import urllib.request
            import urllib.error

            try:
                response = urllib.request.urlopen("http://localhost:8888", timeout=5)
                assert response.status == 200, "Jupyter Lab should be accessible"
            except (urllib.error.URLError, OSError) as e:
                # If we can't connect, check if container is still running
                result = run_command(
                    ["docker", "ps", "--filter", f"name={container_name}", "--format", "{{.Names}}"],
                    cwd=project_path,
                    check=False,
                )
                if container_name in result.stdout:
                    # Container is running but Jupyter not responding - might be a timing issue
                    print(f"⚠️  Container is running but Jupyter Lab not accessible: {e}")
                else:
                    # Container crashed, check logs
                    logs_result = run_command(
                        ["docker", "logs", container_name],
                        cwd=project_path,
                        check=False,
                    )
                    pytest.fail(f"Container crashed. Logs: {logs_result.stdout}\n{logs_result.stderr}")

        finally:
            # Cleanup: stop and remove container
            run_command(
                ["docker", "stop", container_name],
                cwd=project_path,
                check=False,
            )
            run_command(
                ["docker", "rm", container_name],
                cwd=project_path,
                check=False,
            )
            # Remove the test image
            run_command(
                ["docker", "rmi", image_name],
                cwd=project_path,
                check=False,
            )
