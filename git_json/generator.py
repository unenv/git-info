import json
import subprocess
from datetime import datetime
from pathlib import Path


class GitJsonGenerator:
    def generate_git_json(self, package_path: str = "resources"):
        target_dir = Path(package_path)
        target_dir.mkdir(parents=True, exist_ok=True)
        
        git_json = {
            "git.branch": self.run_git_command("git rev-parse --abbrev-ref HEAD"),
            "git.build.host": subprocess.run("hostname", shell=True, capture_output=True, text=True).stdout.strip(),
            "git.build.time": datetime.now().strftime("%d.%m.%Y @ %H:%M:%S %Z"),
            "git.build.user.email": self.run_git_command("git config user.email"),
            "git.build.user.name": self.run_git_command("git config user.name"),
            "git.build.version": "1.0.0",
            "git.closest.tag.commit.count": self.run_git_command("git describe --tags --abbrev=0 --match='*' --always"),
            "git.closest.tag.name": self.run_git_command("git describe --tags --abbrev=0 --match='*' --always"),
            "git.commit.author.time": self.run_git_command('git log -1 --format=%ad --date=format:"%d.%m.%Y @ %H:%M:%S "'),
            "git.commit.committer.time": self.run_git_command('git log -1 --format=%cd --date=format:"%d.%m.%Y @ %H:%M:%S "'),
            "git.commit.id": self.run_git_command("git rev-parse HEAD"),
            "git.commit.id.abbrev": self.run_git_command("git rev-parse --short HEAD"),
            "git.commit.id.describe": self.run_git_command("git describe --always --dirty"),
            "git.commit.id.describe-short": self.run_git_command("git describe --always --dirty --abbrev=10"),
            "git.commit.message.full": self.run_git_command("git log -1 --format=%B").replace("\n", "\\n"),
            "git.commit.message.short": self.run_git_command("git log -1 --format=%s"),
            "git.commit.time": self.run_git_command('git log -1 --format=%cd --date=format:"%d.%m.%Y @ %H:%M:%S "'),
            "git.commit.user.email": self.run_git_command("git log -1 --format=%ae"),
            "git.commit.user.name": self.run_git_command("git log -1 --format=%an"),
            "git.dirty": "true" if self.run_git_command("git diff --quiet; echo $?") == "1" else "false",
            "git.local.branch.ahead": self.run_git_command("git rev-list --count HEAD@{upstream}..HEAD 2>/dev/null || echo 0"),
            "git.local.branch.behind": self.run_git_command("git rev-list --count HEAD...HEAD@{upstream} 2>/dev/null || echo 0"),
            "git.remote.origin.url": self.run_git_command("git config --get remote.origin.url"),
            "git.tags": self.run_git_command("git tag --points-at HEAD"),
            "git.total.commit.count": self.run_git_command("git rev-list --count HEAD")
        }
        
        json_file = target_dir / "git.json"
        with open(json_file, "w") as f:
            json.dump(git_json, f, indent=4)
        
        print(f"Generated git info: {json_file.absolute()}")

    def run_git_command(self, cmd: str) -> str:
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return ""