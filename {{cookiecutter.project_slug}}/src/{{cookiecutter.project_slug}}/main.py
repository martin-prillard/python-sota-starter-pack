{% if cookiecutter.project_type == "fastapi" %}
"""FastAPI application with MCP endpoint."""

from fastapi import FastAPI
from pydantic import BaseModel

try:
    from fastmcp import FastMCP
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False

app = FastAPI(
    title="{{ cookiecutter.project_name }}",
    description="{{ cookiecutter.project_description }}",
    version="0.1.0",
)

if MCP_AVAILABLE:
    try:
        mcp = FastMCP("{{ cookiecutter.project_slug }}")

        @mcp.tool()
        def example_tool(query: str) -> str:
            """Example MCP tool."""
            return f"Processed: {query}"

        # Try to include router - FastMCP API may vary by version
        # Use getattr to safely access router without raising AttributeError
        router = getattr(mcp, "router", None)
        if router is None:
            # Try alternative methods
            get_router = getattr(mcp, "get_router", None)
            if get_router:
                router = get_router()
            else:
                as_router = getattr(mcp, "as_router", None)
                if as_router:
                    router = as_router()
        
        if router is not None:
            app.include_router(router)
    except Exception:
        # If MCP setup fails or router is not available, continue without it
        # The MCP tools may still be registered via other mechanisms
        pass


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str
    version: str


@app.get("/", tags=["root"])
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": "{{ cookiecutter.project_name }} API"}


@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(status="healthy", version="0.1.0")
{% elif cookiecutter.project_type == "streamlit" %}
"""Streamlit application."""

import streamlit as st
from pydantic import BaseModel, ValidationError


class ExampleModel(BaseModel):
    """Example Pydantic model."""

    name: str
    value: int


def main() -> None:
    """Main Streamlit application."""
    st.set_page_config(
        page_title="{{ cookiecutter.project_name }}",
        page_icon="🚀",
        layout="wide",
    )

    st.title("{{ cookiecutter.project_name }}")
    st.write("{{ cookiecutter.project_description }}")

    with st.form("example_form"):
        name = st.text_input("Name", value="Example")
        value = st.number_input("Value", min_value=0, value=42)
        submitted = st.form_submit_button("Submit")

        if submitted:
            try:
                model = ExampleModel(name=name, value=value)
                st.success(f"Created model: {model.model_dump_json()}")
            except ValidationError as e:
                st.error(f"Validation error: {e}")


if __name__ == "__main__":
    main()
{% else %}
"""Main module for {{ cookiecutter.project_slug }}."""

from {{ cookiecutter.project_slug|replace('-', '_') }} import __version__


def main() -> str:
    """Main function."""
    return f"{{ cookiecutter.project_name }} v{__version__}"


if __name__ == "__main__":
    print(main())
{% endif %}
