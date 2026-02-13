# Python SOTA Starter Pack

A modern, best-practice Python project template using Cookiecutter. This template generates four types of Python projects:

1. **Python Library** - For building and publishing packages to PyPI
2. **FastAPI API** - REST API with MCP (Model Context Protocol) endpoint support
3. **Streamlit Webapp** - Interactive web applications
4. **Data Science Project** - Jupyter Lab based data science projects

## Features

- 🚀 **Modern Tooling**: uv, hatch, ruff, black, mypy, ty, bandit
- 📦 **Best Practices**: pyproject.toml, type hints, Pydantic
- 🐳 **Docker Support**: Multi-stage Dockerfiles
- 🔄 **CI/CD**: GitLab CI/CD with linting, testing, security scanning, and SonarQube
- 📚 **Documentation**: MkDocs for API documentation
- 🔒 **Pre-commit Hooks**: Automated code quality checks
- 💻 **Dev Container**: VS Code devcontainer configuration
- ✅ **Testing**: pytest with coverage reporting

## Prerequisites

- Python 3.12+
- [Cookiecutter](https://cookiecutter.readthedocs.io/) installed:
  ```bash
  pip install cookiecutter
  ```
- [uv](https://github.com/astral-sh/uv)

## Usage

### Generate a New Project

```bash
cookiecutter .
```

You'll be prompted for:

- **project_name**: Name of your project
- **project_description**: Brief description
- **author_name**: Your name
- **author_email**: Your email
- **project_type**: Choose from `library`, `fastapi`, `streamlit`, or `datascience` (type exactly as shown)
- **python_version**: Python version (default: 3.12)
- **use_docker**: Whether to include Docker support (yes/no)
- **publish_to_pypi**: Whether to configure PyPI publishing (yes/no)
- **pypi_username**: PyPI username (if publishing)
- **pypi_token**: PyPI token (if publishing)
- **gitlab_url**: Your GitLab instance URL
- **gitlab_group**: Your GitLab group/namespace
- **sonarqube_token**: SonarQube token (optional)

### After Generation

```bash
cd <your-project-slug>
uv sync
pre-commit install
```

## Project Types

### Python Library

A standard Python package ready for PyPI publishing:

```bash
# Build
python -m build

# Publish (if configured)
twine upload dist/*
```

### FastAPI API

Includes FastAPI with MCP endpoint support using FastMCP:

```bash
# Run locally
uvicorn <project_slug>.main:app --reload
```

### Streamlit Webapp

Interactive web application:

```bash
# Run locally
streamlit run <project_slug>/main.py
```

### Data Science Project

Jupyter Lab based project with data science libraries:

```bash
# Run locally
jupyter lab
```

## Tools Included

- **uv**: Fast Python package installer
- **hatch**: Modern build backend
- **ruff**: Fast linter and formatter
- **black**: Code formatter (via ruff)
- **mypy**: Static type checker
- **ty**: Type checking tool
- **bandit**: Security linter
- **pytest**: Testing framework
- **pre-commit**: Git hooks
- **mkdocs**: Documentation (library, fastapi, streamlit)
- **Pydantic**: Data validation

## CI/CD Pipeline

The GitLab CI/CD pipeline includes:

- **Lint**: ruff check and format
- **Test**: pytest with coverage
- **Security**: bandit scanning
- **Build**: Package/Docker image building
- **Deploy**: PyPI publishing (if configured)
- **Quality**: SonarQube analysis

## License

MIT

## Contributing

Contributions welcome! Please ensure all code follows the project's style guidelines and passes all pre-commit hooks.
