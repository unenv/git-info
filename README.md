# git-json
[![codecov](https://codecov.io/github/unenv/git-json/graph/badge.svg?token=0QQ7JROLWL)](https://codecov.io/github/unenv/git-json)
[![PyPI version](https://img.shields.io/pypi/v/git-json)](https://pypi.org/project/git-json/)
![Python versions](https://img.shields.io/pypi/pyversions/git-json)

A Python tool to generate comprehensive git information for your projects.

## Installation

```bash
pip install git-json
```

## Usage

### Command Line

```bash
# Generate git info to default 'resources' directory
git-json

# Generate git info to custom directory
git-json --package-path my-resources
```

### Python API

```python
from git_json import GitJsonGenerator

generator = GitJsonGenerator()
generator.generate_git_json("output-directory")
```

### Configuration

You can set a default output path in your `pyproject.toml`:

```toml
[tool.git-json]
path = "my-custom-path"
```

This is useful when using git-json as a poetry script:

```toml
[tool.poetry.scripts]
git-json = "git_json.cli:main"

[tool.git-json]
path = "src/resources"
```

## Output

Generates a `git.json` file with comprehensive git information including:

- Branch information
- Commit details (hash, message, author, time)
- Build information (host, time, user)
- Repository status (dirty, ahead/behind)
- Tags and version information

## Development

```bash
# Install dependencies
poetry install --with dev

# Run tests
poetry run pytest

# Run linting
poetry run ruff check .

# Generate git info
poetry run git-json
```