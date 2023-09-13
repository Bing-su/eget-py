import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def get_version() -> str:
    root = Path(__file__).parent
    init = root.joinpath("eget", "__init__.py").read_text("utf-8")
    version = re.search(r'__version__ = "(.*?)"', init)
    if not version:
        msg = "could not find version in __init__.py"
        raise RuntimeError(msg)
    return version.group(1)


def download(output: str) -> None:
    go = shutil.which("go")
    git = shutil.which("git")

    if go is None:
        msg = "golang is required and 'go' should be in $PATH"
        raise RuntimeError(msg)

    if git is None:
        msg = "git is required and 'git' should be in $PATH"
        raise RuntimeError(msg)

    version = get_version()

    repo = "github.com/zyedidia/eget"
    github = f"https://{repo}"

    with tempfile.TemporaryDirectory() as tmp_dir:
        try:
            subprocess.run(
                [git, "clone", "-b", f"v{version}", "--depth", "1", github, tmp_dir],
                check=True,
            )
        except subprocess.CalledProcessError as e:
            msg = "git clone failed"
            raise RuntimeError(msg) from e

        args = [
            go,
            "build",
            "-trimpath",
            "-ldflags",
            f"-s -v -X main.Version={version}",
            "-o",
            output,
            ".",
        ]

        try:
            subprocess.run(args, check=True, cwd=tmp_dir)
        except subprocess.CalledProcessError as e:
            msg = "eget build failed"
            raise RuntimeError(msg) from e


def pdm_build_initialize(context):
    if context.target == "sdist":
        return
    context.ensure_build_dir()
    output_path = Path(context.build_dir, "eget", "eget")
    if sys.platform == "win32":
        output_dir = output_path.with_suffix(".exe")
    download(str(output_dir))
