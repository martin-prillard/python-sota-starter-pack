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
- [uv](https://github.com/astral-sh/uv)

## Usage

### Generate a New Project

**Recommended: Use the custom generator script for conditional prompts:**

```bash
python generate.py
```

Or use cookiecutter directly (note: all fields will be prompted, press Enter to skip optional ones):

```bash
uvx cookiecutter .
```

**Note:** When using `uvx cookiecutter .` directly, you'll be prompted for all fields. For conditional prompts (only showing relevant fields), use `python generate.py` instead.

**Prompts (when using generate.py, conditional prompts only shown when relevant):**

- **project_name**: Name of your project
- **project_slug**: Project slug (auto-generated from name)
- **project_description**: Brief description
- **author_name**: Your name
- **author_email**: Your email
- **project_type**: Choose from `library`, `fastapi`, `streamlit`, or `datascience`
- **python_version**: Python version (default: 3.12)
- **use_docker**: Whether to include Docker support (yes/no)
- **publish_to_pypi**: Whether to configure PyPI publishing (yes/no)
  - **pypi_username**: PyPI username (only asked if publishing to PyPI)
  - **pypi_token**: PyPI token (only asked if publishing to PyPI)
- **use_ci**: Whether to configure CI/CD (yes/no)
  - **git_provider**: Choose `gitlab` or `github` (only asked if using CI)
  - **gitlab_url**: GitLab instance URL (only asked if using GitLab)
  - **gitlab_group**: GitLab group/namespace (only asked if using GitLab)
  - **github_org**: GitHub organization/username (only asked if using GitHub)
  - **sonarqube_token**: SonarQube token (optional, only asked if using CI)

### After Generation

1. Navigate to your project:
   ```bash
   cd <your-project-slug>
   ```

2. Install dependencies with uv (including dev dependencies):
   ```bash
   uv sync --extra dev
   ```

3. Install pre-commit hooks:
   ```bash
   uv run pre-commit install
   ```

4. Run tests:
   ```bash
   pytest
   ```

## Project Types

### Python Library

A standard Python package ready for PyPI publishing:

```bash
# Build package
python -m build

# Run tests
pytest

# Publish (if configured)
twine upload dist/*
```

### FastAPI API

Includes FastAPI with MCP endpoint support using FastMCP:

```bash
# Run development server
uvicorn <project_slug>.main:app --reload

# Access API docs
# http://localhost:8000/docs
```

### Streamlit Webapp

Interactive web application:

```bash
# Run app
streamlit run <project_slug>/main.py

# Access app
# http://localhost:8501
```

### Data Science Project

Jupyter Lab based project with data science libraries:

```bash
# Start Jupyter Lab
jupyter lab

# Access Jupyter
# http://localhost:8888
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

## Docker (if enabled)

```bash
# Build image
docker build -t <project-slug>:latest .

# Run container
docker run -p 8000:8000 <project-slug>:latest
```

## CI/CD Pipeline

The GitLab CI/CD pipeline includes:

- **Lint**: ruff check and format
- **Test**: pytest with coverage
- **Security**: bandit scanning
- **Build**: Package/Docker image building
- **Deploy**: PyPI publishing (if configured)
- **Quality**: SonarQube analysis

### CI/CD Setup

1. Push to GitLab
2. Configure CI/CD variables in GitLab:
   - `PYPI_USERNAME` (if publishing to PyPI)
   - `PYPI_TOKEN` (if publishing to PyPI)
   - `SONARQUBE_TOKEN` (for SonarQube analysis)

3. The pipeline will automatically:
   - Lint and format code
   - Run tests with coverage
   - Scan for security issues
   - Build Docker images (if enabled)
   - Publish to PyPI (if configured)

## Development Workflow

1. Create a feature branch
2. Make changes
3. Pre-commit hooks will run automatically
4. Commit and push
5. Create merge request
6. CI/CD pipeline runs automatically
7. Merge after approval

## Testing the Template

The template includes end-to-end tests that verify each project type works correctly. To run the tests:

1. Install template dependencies:
   ```bash
   uv sync --extra dev
   ```

2. Run all end-to-end tests:
   ```bash
   # Using uv
   uv run pytest tests/test_e2e.py -v
   ```

3. Run tests for a specific project type:
   ```bash
   uv run pytest tests/test_e2e.py::TestLibraryProject -v
   uv run pytest tests/test_e2e.py::TestFastAPIProject -v
   uv run pytest tests/test_e2e.py::TestStreamlitProject -v
   uv run pytest tests/test_e2e.py::TestDataScienceProject -v
   ```

4. Clean test artifacts manually (if needed):
   ```bash
   # Remove any test-* directories in the current folder
   rm -rf test-library test-fastapi test-streamlit test-datascience
   ```

The end-to-end tests will:
- Generate a project for each type (library, fastapi, streamlit, datascience)
- Install dependencies using `uv sync --extra dev`
- Install pre-commit hooks
- Run pytest to verify tests pass
- Run linting and type checking
- Verify project-specific commands work (e.g., uvicorn for FastAPI, streamlit for Streamlit apps)
- Build packages for library projects

**Note:** Tests use temporary directories and clean up after themselves, but if tests are interrupted, you may need to manually clean up `test-*` directories.

## License

MIT

## Contributing

Contributions welcome! Please ensure all code follows the project's style guidelines and passes all pre-commit hooks.
