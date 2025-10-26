import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from git_json.cli import main


def test_cli_default_path():
    mock_responses = {"git rev-parse HEAD": "abc123", "hostname": "test-host"}
    
    def mock_subprocess_run(cmd, **kwargs):
        result = MagicMock()
        result.stdout = mock_responses.get(cmd, "")
        result.returncode = 0
        return result
    
    with patch('subprocess.run', side_effect=mock_subprocess_run), \
         patch('sys.argv', ['git-json']), \
         tempfile.TemporaryDirectory() as temp_dir:
        
        with patch('git_json.generator.Path') as mock_path:
            mock_path.return_value = Path(temp_dir)
            main()


def test_cli_custom_path():
    mock_responses = {"git rev-parse HEAD": "abc123", "hostname": "test-host"}
    
    def mock_subprocess_run(cmd, **kwargs):
        result = MagicMock()
        result.stdout = mock_responses.get(cmd, "")
        result.returncode = 0
        return result
    
    with patch('subprocess.run', side_effect=mock_subprocess_run), \
         patch('sys.argv', ['git-json', '--package-path', 'custom-dir']), \
         tempfile.TemporaryDirectory() as temp_dir:
        
        with patch('git_json.generator.Path') as mock_path:
            mock_path.return_value = Path(temp_dir)
            main()

def test_get_default_path_from_pyproject():
    """Test reading path from pyproject.toml."""
    from git_json.cli import _get_default_path
    import tempfile
    import os
    
    pyproject_content = b'[tool.git-json]\npath = "custom/path"\n'
    
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.toml') as f:
        f.write(pyproject_content)
        f.flush()
        
        # Change to the temp file's directory
        original_cwd = os.getcwd()
        temp_dir = os.path.dirname(f.name)
        pyproject_path = os.path.join(temp_dir, 'pyproject.toml')
        os.rename(f.name, pyproject_path)
        
        try:
            os.chdir(temp_dir)
            result = _get_default_path()
            assert result == "custom/path"
        finally:
            os.chdir(original_cwd)
            os.unlink(pyproject_path)


def test_get_default_path_fallback():
    """Test fallback when no pyproject.toml exists."""
    from git_json.cli import _get_default_path
    
    with patch('git_json.cli.Path') as mock_path:
        mock_path.return_value.exists.return_value = False
        result = _get_default_path()
        assert result == "resources"