#!/usr/bin/env python3

import argparse
from pathlib import Path
from .generator import GitJsonGenerator

try:
    import tomllib
except ImportError:
    import tomli as tomllib

def _get_default_path():
    """Get default path from pyproject.toml or fallback."""
    try:
        pyproject_path = Path("pyproject.toml")
        if pyproject_path.exists():
            with open(pyproject_path, "rb") as f:
                data = tomllib.load(f)
                return data.get("tool", {}).get("git-json", {}).get("path", "resources")
    except Exception:
        pass
    return "resources"

def main():
    """Generate git info."""
    parser = argparse.ArgumentParser(description="Generate git info")
    default_path = _get_default_path()
    parser.add_argument("--package-path", default=default_path, 
                       help=f"Package path for git info output (default: {default_path})")
    args = parser.parse_args()
    
    generator = GitJsonGenerator()
    generator.generate_git_json(args.package_path)

if __name__ == "__main__":
    main()