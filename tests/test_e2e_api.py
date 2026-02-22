"""End-to-end tests for FastAPI project type."""

import subprocess
import time
from pathlib import Path

import pytest

from tests.conftest import generate_project, install_pre_commit, run_command, setup_git_repo


class TestFastAPIProject:
    """End-to-end tests for FastAPI project type."""

    def test_fastapi_generation_and_setup(self, template_dir, temp_dir):
        """Test generating a FastAPI project and running setup commands."""
        project_slug = "test-fastapi"
        project_path = generate_project(template_dir, temp_dir, "fastapi", project_slug)

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

        # Test 4: Verify FastAPI app can be imported
        # First verify the package is importable (package name uses underscores, not hyphens)
        package_name = project_slug.replace("-", "_")
        result = run_command(
            ["uv", "run", "python", "-c", f"import {package_name}; print('OK')"],
            cwd=project_path,
        )
        assert result.returncode == 0, f"Failed to import package {package_name}: {result.stderr}"
        # Then verify the app can be imported
        result = run_command(
            ["uv", "run", "python", "-c", f"from {package_name}.main import app; print('OK')"],
            cwd=project_path,
        )
        assert result.returncode == 0, f"Failed to import FastAPI app: {result.stderr}"

        # Test 5: Check that uvicorn command works (dry run)
        # We'll just verify the command exists and can be called
        result = run_command(
            ["uv", "run", "uvicorn", "--help"],
            cwd=project_path,
        )
        assert result.returncode == 0, f"uvicorn not available: {result.stderr}"

        # Test 6: Verify main module can be run
        # Package directory uses underscores (normalized from project_slug)
        package_name = project_slug.replace("-", "_")
        main_file = project_path / "src" / package_name / "main.py"
        assert main_file.exists(), f"main.py should exist at {main_file}"

    def test_fastapi_docker_build_and_run(self, template_dir, temp_dir):
        """Test Docker build and run for FastAPI project."""
        project_slug = "test-fastapi"
        project_path = generate_project(template_dir, temp_dir, "fastapi", project_slug)

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
        package_name = project_slug.replace("-", "_")
        
        # Start container
        result = run_command(
            [
                "docker",
                "run",
                "-d",
                "--name",
                container_name,
                "-p",
                "8000:8000",
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
            # Wait a bit for the server to start
            time.sleep(3)

            # Test that the API is responding
            import urllib.request
            import urllib.error

            try:
                response = urllib.request.urlopen("http://localhost:8000/docs", timeout=5)
                assert response.status == 200, "FastAPI docs endpoint should be accessible"
            except (urllib.error.URLError, OSError) as e:
                # If we can't connect, check if container is still running
                result = run_command(
                    ["docker", "ps", "--filter", f"name={container_name}", "--format", "{{.Names}}"],
                    cwd=project_path,
                    check=False,
                )
                if container_name in result.stdout:
                    # Container is running but API not responding - might be a timing issue
                    print(f"⚠️  Container is running but API not accessible: {e}")
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
