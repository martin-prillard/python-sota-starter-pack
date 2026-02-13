"""Core functionality for {{ cookiecutter.project_slug }}."""

from pydantic import BaseModel


{% if cookiecutter.project_type == "library" %}
class ExampleModel(BaseModel):
    """Example Pydantic model for the library."""

    name: str
    value: int

    def process(self) -> str:
        """Process the model."""
        return f"{self.name}: {self.value}"
{% else %}
def example_function() -> str:
    """Example function."""
    return "Hello from {{ cookiecutter.project_slug|replace('-', '_') }}"
{% endif %}
