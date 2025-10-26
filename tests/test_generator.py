import json
import re
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from git_json.generator import GitJsonGenerator


def test_generate_git_json_subprocess_error():
    """Test generator handles subprocess errors gracefully"""
    def mock_subprocess_run(cmd, **kwargs):
        if "git rev-parse HEAD" in cmd:
            raise subprocess.CalledProcessError(1, cmd)
        result = MagicMock()
        result.stdout = "test-host" if "hostname" in cmd else ""
        result.returncode = 0
        return result
    
    with patch('subprocess.run', side_effect=mock_subprocess_run):
        generator = GitJsonGenerator()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            generator.generate_git_json(temp_dir)
            
            git_json_path = Path(temp_dir) / "git.json"
            assert git_json_path.exists()
            
            with open(git_json_path) as f:
                git_json = json.load(f)
            
            # Should have empty string for failed git command
            assert git_json["git.commit.id"] == ""


def test_generate_git_json():
    mock_responses = {
        "git rev-parse --abbrev-ref HEAD": "main",
        "hostname": "test-host",
        "git config user.email": "test@example.com",
        "git config user.name": "Test User",
        "git describe --tags --abbrev=0 --match='*' --always": "v1.0.0",
        'git log -1 --format=%ad --date=format:"%d.%m.%Y @ %H:%M:%S "': "01.01.2024 @ 12:00:00 ",
        'git log -1 --format=%cd --date=format:"%d.%m.%Y @ %H:%M:%S "': "01.01.2024 @ 12:00:00 ",
        "git rev-parse HEAD": "abc123def456",
        "git rev-parse --short HEAD": "abc123d",
        "git describe --always --dirty": "v1.0.0-1-gabc123d",
        "git describe --always --dirty --abbrev=10": "v1.0.0-1-gabc123def4",
        "git log -1 --format=%B": "Initial commit",
        "git log -1 --format=%s": "Initial commit",
        "git log -1 --format=%ae": "author@example.com",
        "git log -1 --format=%an": "Author Name",
        "git diff --quiet; echo $?": "0",
        "git rev-list --count HEAD@{upstream}..HEAD 2>/dev/null || echo 0": "0",
        "git rev-list --count HEAD...HEAD@{upstream} 2>/dev/null || echo 0": "0",
        "git config --get remote.origin.url": "https://github.com/test/repo.git",
        "git tag --points-at HEAD": "v1.0.0",
        "git rev-list --count HEAD": "42"
    }
    
    def mock_subprocess_run(cmd, **kwargs):
        result = MagicMock()
        result.stdout = mock_responses.get(cmd, "")
        result.returncode = 0
        return result
    
    with patch('subprocess.run', side_effect=mock_subprocess_run):
        generator = GitJsonGenerator()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            generator.generate_git_json(temp_dir)
            
            git_json_path = Path(temp_dir) / "git.json"
            assert git_json_path.exists()
            
            with open(git_json_path) as f:
                git_json = json.load(f)
            
            # Test all 25 keys exist
            expected_keys = [
                "git.branch", "git.build.host", "git.build.time", "git.build.user.email",
                "git.build.user.name", "git.build.version", "git.closest.tag.commit.count",
                "git.closest.tag.name", "git.commit.author.time", "git.commit.committer.time",
                "git.commit.id", "git.commit.id.abbrev", "git.commit.id.describe",
                "git.commit.id.describe-short", "git.commit.message.full", "git.commit.message.short",
                "git.commit.time", "git.commit.user.email", "git.commit.user.name",
                "git.dirty", "git.local.branch.ahead", "git.local.branch.behind",
                "git.remote.origin.url", "git.tags", "git.total.commit.count"
            ]
            assert len(git_json) == 25
            for key in expected_keys:
                assert key in git_json
            
            # Test mocked values
            assert git_json["git.branch"] == "main"
            assert git_json["git.build.host"] == "test-host"
            assert re.match(r"\d{2}\.\d{2}\.\d{4} @ \d{2}:\d{2}:\d{2}", git_json["git.build.time"])
            assert git_json["git.build.user.email"] == "test@example.com"
            assert git_json["git.build.user.name"] == "Test User"
            assert git_json["git.build.version"] == "1.0.0"
            assert git_json["git.commit.id"] == "abc123def456"
            assert git_json["git.commit.id.abbrev"] == "abc123d"
            assert git_json["git.commit.message.full"] == "Initial commit"
            assert git_json["git.commit.message.short"] == "Initial commit"
            assert git_json["git.dirty"] == "false"
            assert git_json["git.total.commit.count"] == "42"