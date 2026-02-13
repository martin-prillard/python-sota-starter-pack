"""Main entry point for {{ cookiecutter.project_slug }}."""

{% if cookiecutter.project_type == "fastapi" %}
import uvicorn
from {{ cookiecutter.project_slug }}.main import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
{% elif cookiecutter.project_type == "streamlit" %}
import streamlit.web.cli as stcli
import sys

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", "{{ cookiecutter.project_slug }}/main.py"]
    sys.exit(stcli.main())
{% else %}
def main() -> None:
    """Main entry point."""
    print("{{ cookiecutter.project_name }}")

if __name__ == "__main__":
    main()
{% endif %}
