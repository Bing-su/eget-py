import re
import os
import shutil
import subprocess
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

    if go is None:
        msg = "golang is required and 'go' should be in $PATH"
        raise RuntimeError(msg)

    os.environ["GOBIN"] = output
    version = get_version()

    repo = "github.com/zyedidia/eget"
    args = [
        go,
        "install",
        "-trimpath",
        "-ldflags",
        f"-s -v -X main.Version={version}",
        f"{repo}@v{version}",
    ]

    try:
        subprocess.run(args, check=True)
    except subprocess.CalledProcessError as e:
        msg = "Go install failed"
        raise RuntimeError(msg) from e


def pdm_build_initialize(context):
    if context.target == "sdist":
        return
    context.ensure_build_dir()
    output_dir = Path(context.build_dir, "eget")
    download(str(output_dir))
