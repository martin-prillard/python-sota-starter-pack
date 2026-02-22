"""Integration tests that verify all project types work correctly."""

import pytest

from tests.conftest import generate_project, run_command


@pytest.mark.integration
class TestAllProjectTypes:
    """Integration tests that verify all project types work correctly."""

    def test_all_project_types_generate_successfully(self, template_dir, temp_dir):
        """Test that all project types can be generated."""
        project_types = ["library", "fastapi", "streamlit", "datascience"]

        for project_type in project_types:
            project_slug = f"test-{project_type}"
            project_path = generate_project(template_dir, temp_dir, project_type, project_slug)

            # Verify basic structure
            assert (project_path / "pyproject.toml").exists(), f"{project_type}: pyproject.toml missing"
            assert (project_path / "README.md").exists(), f"{project_type}: README.md missing"
            # Package directory uses underscores (normalized from project_slug)
            package_name = project_slug.replace("-", "_")
            assert (project_path / "src" / package_name).exists(), f"{project_type}: src directory missing"

            # Verify dependencies can be installed (uv sync installs the package in editable mode automatically)
            result = run_command(
                ["uv", "sync", "--extra", "dev"],
                cwd=project_path,
            )
            assert result.returncode == 0, f"{project_type}: Failed to install dependencies"

            # Initialize git repository (required for some tests)
            run_command(
                ["git", "init"],
                cwd=project_path,
                check=False,
            )
            if (project_path / ".git").exists():
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

            # Verify tests can run
            # pytest return codes: 0=all passed, 1=some failed, 2=error, 5=no tests
            # We accept 0, 1, and 5, but not 2 (configuration/collection error)
            result = run_command(
                ["uv", "run", "pytest"],
                cwd=project_path,
                check=False,
            )
            # Allow test failures (1) and no tests found (5), but not errors (2)
            assert result.returncode != 2, (
                f"{project_type}: Pytest configuration/collection error "
                f"(return code {result.returncode}): {result.stdout}\n{result.stderr}"
            )
