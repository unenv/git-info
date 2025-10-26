#!/usr/bin/env python3

import argparse
from pathlib import Path
from .generator import GitJsonGenerator

try:
    import tomllib
except ImportError:
    import tomli as tomllib

def _get_default_paths():
    """Get default paths from pyproject.toml or fallback."""
    try:
        pyproject_path = Path("pyproject.toml")
        if pyproject_path.exists():
            with open(pyproject_path, "rb") as f:
                data = tomllib.load(f)
                path_config = data.get("tool", {}).get("git-json", {}).get("path", "resources")
                return path_config if isinstance(path_config, list) else [path_config]
    except Exception:
        pass
    return ["resources"]

def main():
    """Generate git info."""
    parser = argparse.ArgumentParser(description="Generate git info")
    default_paths = _get_default_paths()
    parser.add_argument("--package-path", 
                       help="Package path for git info output")
    args = parser.parse_args()
    
    generator = GitJsonGenerator()
    
    if args.package_path:
        generator.generate_git_json(args.package_path)
    else:
        for path in default_paths:
            generator.generate_git_json(path)

if __name__ == "__main__":
    main()