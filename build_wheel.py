import os
import subprocess
import sys


def build(os_: str, arch: str, platform: str):
    os.environ["GOOS"] = os_
    os.environ["GOARCH"] = arch

    args = [
        sys.executable,
        "-m",
        "build",
        "-w",
        f"--config-setting=--plat-name={platform}",
    ]

    subprocess.run(args, check=True)


def main():
    matrix = [
        ("windows", "amd64", "win_amd64"),
        ("darwin", "amd64", "macosx_10_7_x86_64"),
        ("darwin", "arm64", "macosx_11_0_arm64"),
        ("linux", "amd64", "manylinux_2_17_x86_64"),
        ("linux", "amd64", "musllinux_1_1_x86_64"),
        ("linux", "arm64", "manylinux_2_17_aarch64"),
        ("linux", "arm64", "musllinux_1_1_aarch64"),
        ("linux", "s390x", "manylinux_2_17_s390x"),
        ("linux", "ppc64le", "manylinux_2_17_ppc64le"),
    ]

    for os_, arch, platform in matrix:
        build(os_, arch, platform)


if __name__ == "__main__":
    main()
