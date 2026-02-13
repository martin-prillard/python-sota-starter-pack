#!/bin/bash
# Script to install dependencies and run all end-to-end tests

set -e  # Exit on error

echo "Installing template dependencies..."
uv sync --extra dev

echo ""
echo "Running all end-to-end tests..."
uv run pytest tests/test_e2e.py -v

echo ""
echo "Running tests for Library project type..."
uv run pytest tests/test_e2e.py::TestLibraryProject -v

echo ""
echo "Running tests for FastAPI project type..."
uv run pytest tests/test_e2e.py::TestFastAPIProject -v

echo ""
echo "Running tests for Streamlit project type..."
uv run pytest tests/test_e2e.py::TestStreamlitProject -v

echo ""
echo "Running tests for DataScience project type..."
uv run pytest tests/test_e2e.py::TestDataScienceProject -v

echo ""
echo "All tests completed successfully!"
