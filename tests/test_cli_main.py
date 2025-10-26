import subprocess
import sys
import tempfile
from pathlib import Path


def test_cli_main_execution():
    """Test CLI main execution as subprocess"""
    with tempfile.TemporaryDirectory() as temp_dir:
        result = subprocess.run([
            sys.executable, '-m', 'git_json.cli',
            '--package-path', temp_dir
        ], capture_output=True, text=True)
        
        # Should succeed (exit code 0) and create git.json
        assert result.returncode == 0
        assert (Path(temp_dir) / 'git.json').exists()