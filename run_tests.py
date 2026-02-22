#!/usr/bin/env python3
"""Script to run all end-to-end tests."""

import subprocess
import sys
from pathlib import Path

def main():
    """Run all tests."""
    project_root = Path(__file__).parent
    tests_dir = project_root / "tests"
    
    print("Running all end-to-end tests...")
    print(f"Project root: {project_root}")
    print(f"Tests directory: {tests_dir}")
    print()
    
    # Run pytest
    result = subprocess.run(
        ["uv", "run", "pytest", str(tests_dir), "-v", "--tb=short"],
        cwd=project_root,
    )
    
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
