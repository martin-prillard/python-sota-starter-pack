# Quick Start Guide

## Installation

1. Generate a new project:
   ```bash
   uvx cookiecutter .
   ```

## Project Type Options

When prompted for `project_type`, choose one of:
- `library` - Python library/package for PyPI
- `fastapi` - FastAPI REST API with MCP endpoints
- `streamlit` - Streamlit web application
- `datascience` - Jupyter Lab data science project

## After Generation

1. Navigate to your project:
   ```bash
   cd <project-slug>
   ```

2. Install dependencies with uv:
   ```bash
   uv sync
   ```

3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

4. Run tests:
   ```bash
   pytest
   ```

## Project-Specific Commands

### Library
```bash
# Build package
python -m build

# Run tests
pytest
```

### FastAPI
```bash
# Run development server
uvicorn <project_slug>.main:app --reload

# Access API docs
# http://localhost:8000/docs
```

### Streamlit
```bash
# Run app
streamlit run <project_slug>/main.py

# Access app
# http://localhost:8501
```

### Data Science
```bash
# Start Jupyter Lab
jupyter lab

# Access Jupyter
# http://localhost:8888
```

## Docker (if enabled)

```bash
# Build image
docker build -t <project-slug>:latest .

# Run container
docker run -p 8000:8000 <project-slug>:latest
```

## CI/CD Setup

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
