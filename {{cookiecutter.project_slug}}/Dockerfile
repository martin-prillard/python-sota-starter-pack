FROM python:{{ cookiecutter.python_version }}-slim as builder

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock README.md ./

# Install dependencies
RUN uv sync --frozen --no-dev

FROM python:{{ cookiecutter.python_version }}-slim

WORKDIR /app

# Copy uv from builder
COPY --from=builder /usr/local/bin/uv /usr/local/bin/uv

# Copy installed packages
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY src/ ./src/
COPY pyproject.toml ./

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

{% if cookiecutter.project_type == "fastapi" %}
EXPOSE 8000
CMD ["uvicorn", "{{ cookiecutter.project_slug }}.main:app", "--host", "0.0.0.0", "--port", "8000"]
{% elif cookiecutter.project_type == "streamlit" %}
EXPOSE 8501
CMD ["streamlit", "run", "{{ cookiecutter.project_slug }}/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
{% elif cookiecutter.project_type == "datascience" %}
EXPOSE 8888
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]
{% else %}
CMD ["python", "-m", "{{ cookiecutter.python_package_name }}"]
{% endif %}
