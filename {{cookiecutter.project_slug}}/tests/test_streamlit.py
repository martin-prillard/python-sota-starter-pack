"""Tests for Streamlit app models."""

import pytest
from {{ cookiecutter.project_slug|replace('-', '_') }}.main import ExampleModel


def test_example_model() -> None:
    """Test ExampleModel."""
    model = ExampleModel(name="test", value=42)
    assert model.name == "test"
    assert model.value == 42
