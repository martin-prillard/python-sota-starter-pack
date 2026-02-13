# Template Structure

This document describes the structure of the Python SOTA Starter Pack cookiecutter template.

## Root Level Files

- `cookiecutter.json` - Template configuration and variables
- `README.md` - Main documentation
- `QUICKSTART.md` - Quick start guide
- `requirements.txt` - Dependencies for the template itself
- `LICENSE` - MIT License
- `.cookiecutterrc.example` - Example configuration file

## Template Directory: `{{cookiecutter.project_slug}}/`

### Configuration Files

- `pyproject.toml` - Modern Python project configuration with:
  - Hatch build backend
  - Project metadata and dependencies
  - Tool configurations (ruff, black, mypy, pytest, bandit, ty, coverage)
  - Conditional dependencies based on project type

- `.pre-commit-config.yaml` - Pre-commit hooks for:
  - ruff (linting and formatting)
  - mypy (type checking)
  - bandit (security)
  - ty (type checking)
  - Standard pre-commit hooks

- `.gitlab-ci.yml` - CI/CD pipeline with:
  - Linting stage
  - Testing stage with coverage
  - Security scanning
  - Docker build (if enabled)
  - PyPI publishing (if enabled)
  - SonarQube analysis

- `sonar-project.properties` - SonarQube configuration

- `.gitignore` - Comprehensive Python gitignore

- `.dockerignore` - Docker build ignore patterns

### Source Code

- `src/{{cookiecutter.project_slug}}/` - Main package directory
  - `__init__.py` - Package initialization with version
  - `__main__.py` - CLI entry point
  - `main.py` - Project-specific main module (varies by type)
  - `core.py` - Core functionality

### Tests

- `tests/` - Test directory
  - `__init__.py`
  - `test_core.py` - Core functionality tests
  - `test_api.py` - API tests (FastAPI projects)
  - `test_streamlit.py` - Streamlit tests
  - `test_main.py` - Main module tests

### Documentation

- `docs/` - MkDocs documentation (not for datascience projects)
  - `index.md` - Home page
  - `api.md` - API reference

- `mkdocs.yml` - MkDocs configuration

- `README.md` - Project-specific README

- `CHANGELOG.md` - Changelog template

### Docker

- `Dockerfile` - Multi-stage Docker build (if enabled)
- `.dockerignore` - Docker ignore patterns

### Development

- `.devcontainer/devcontainer.json` - VS Code devcontainer configuration

### Data Science (datascience projects only)

- `notebooks/example.ipynb` - Example Jupyter notebook

## Hooks

- `hooks/post_gen_project.py` - Post-generation cleanup script that:
  - Removes irrelevant test files based on project type
  - Removes documentation for datascience projects
  - Removes notebooks for non-datascience projects
  - Removes Docker files if not enabled
  - Cleans up CI/CD configuration

## Project Type Variations

### Library
- Standard Python package structure
- PyPI publishing support
- Full documentation with MkDocs

### FastAPI
- FastAPI application with MCP endpoint support
- Uvicorn server configuration
- API documentation endpoints

### Streamlit
- Streamlit application structure
- Pydantic models for data validation
- Interactive UI components

### Data Science
- Jupyter Lab setup
- Data science libraries (pandas, numpy, matplotlib, seaborn, scikit-learn)
- Example notebooks
- No MkDocs (documentation in notebooks)

## Best Practices Implemented

1. **Modern Python**: Python 3.12+, type hints, Pydantic
2. **Build System**: Hatch (modern, PEP 517/518 compliant)
3. **Package Management**: uv (fast, modern)
4. **Code Quality**: ruff, black, mypy, ty, bandit
5. **Testing**: pytest with coverage
6. **Documentation**: MkDocs with Material theme
7. **CI/CD**: Comprehensive GitLab pipeline
8. **Containerization**: Multi-stage Docker builds
9. **Development**: Dev containers, pre-commit hooks
10. **Security**: Bandit scanning, SonarQube integration
