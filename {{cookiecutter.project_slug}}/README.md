# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Project Type

This is a **{{ cookiecutter.project_type }}** project.

## Quick Start

### Prerequisites

- Python {{ cookiecutter.python_version }} or higher
- [uv](https://github.com/astral-sh/uv)

### Installation

```bash
uv sync
```

### Development Setup

1. Install pre-commit hooks:

```bash
pre-commit install
```

2. Run tests:

```bash
pytest
```

3. Run linting:

```bash
ruff check .
ruff format .
```

4. Run type checking:

```bash
ty check
```

{% if cookiecutter.project_type == "fastapi" %}
### Running the API

```bash
uvicorn {{ cookiecutter.project_slug }}.main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`
{% elif cookiecutter.project_type == "streamlit" %}
### Running the Streamlit App

```bash
streamlit run {{ cookiecutter.project_slug }}/main.py
```

The app will be available at `http://localhost:8501`
{% elif cookiecutter.project_type == "datascience" %}
### Running Jupyter Lab

```bash
jupyter lab
```

Jupyter Lab will be available at `http://localhost:8888`
{% endif %}

{% if cookiecutter.use_docker == "yes" %}
### Docker

Build the Docker image:

```bash
docker build -t {{ cookiecutter.project_slug }}:latest .
```

Run the container:

```bash
docker run -p 8000:8000 {{ cookiecutter.project_slug }}:latest
```
{% endif %}

## Development Tools

This project uses:

- **uv**: Fast Python package installer and resolver
- **hatch**: Modern Python build backend
- **ruff**: Fast Python linter and formatter
- **black**: Code formatter (via ruff)
- **mypy**: Static type checker
- **ty**: Type checking tool
- **bandit**: Security linter
- **pytest**: Testing framework
- **coverage**: Code coverage measurement
- **pre-commit**: Git hooks manager
{% if cookiecutter.project_type != "datascience" %}
- **mkdocs**: Documentation generator
{% endif %}

{% if cookiecutter.use_gitlab_ci == "yes" %}
## CI/CD

This project includes GitLab CI/CD configuration for:

- Linting and formatting checks
- Type checking
- Security scanning (Bandit)
- Testing with coverage
- {% if cookiecutter.publish_to_pypi == "yes" %}PyPI publishing{% endif %}
- {% if cookiecutter.use_docker == "yes" %}Docker image building and publishing{% endif %}
- {% if cookiecutter.project_type != "datascience" %}Documentation building and deployment (GitLab Pages){% endif %}
- SonarQube analysis
{% endif %}

## License

MIT
