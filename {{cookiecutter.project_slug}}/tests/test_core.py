"""Tests for core functionality."""

import pytest
{% if cookiecutter.project_type == "library" %}
from {{ cookiecutter.project_slug|replace('-', '_') }}.core import ExampleModel
{% else %}
from {{ cookiecutter.project_slug|replace('-', '_') }}.core import example_function
{% endif %}


{% if cookiecutter.project_type == "library" %}
def test_example_model() -> None:
    """Test ExampleModel."""
    model = ExampleModel(name="test", value=42)
    assert model.name == "test"
    assert model.value == 42
    assert model.process() == "test: 42"
{% else %}
def test_example_function() -> None:
    """Test example function."""
    result = example_function()
    assert result == "Hello from {{ cookiecutter.project_slug|replace('-', '_') }}"
{% endif %}
