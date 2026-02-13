"""Tests for main module."""

import pytest
from {{ cookiecutter.project_slug }}.main import main


def test_main() -> None:
    """Test main function."""
    result = main()
    assert "{{ cookiecutter.project_name }}" in result
