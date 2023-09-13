import sys
import subprocess
from pathlib import Path


def main():
    exe = Path(__file__).parent.joinpath("eget")
    if sys.platform == "win32":
        exe = exe.with_suffix(".exe")
    subprocess.run([str(exe), *sys.argv[1:]])


if __name__ == "__main__":
    main()
