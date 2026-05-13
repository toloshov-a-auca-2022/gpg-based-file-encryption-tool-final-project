#!/usr/bin/env python3

import argparse
import subprocess
import sys
import os
import getpass
import shutil
from pathlib import Path


class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def ok(msg):
    print(f"{Colors.GREEN}[✓]{Colors.RESET} {msg}")


def err(msg):
    print(f"{Colors.RED}[✗]{Colors.RESET} {msg}", file=sys.stderr)


def info(msg):
    print(f"{Colors.CYAN}[i]{Colors.RESET} {msg}")


def step(msg):
    print(f"{Colors.BLUE}[→]{Colors.RESET} {msg}")


def banner():
    print(f"""
{Colors.BOLD}{Colors.CYAN}╔══════════════════════════════════════════════╗
║        GPG File Encryption Tool v1.0         ║
╚══════════════════════════════════════════════╝{Colors.RESET}
""")


def main():
    banner()

def check_gpg():
    if not shutil.which("gpg"):
        err("GPG is not installed.")
        sys.exit(1)


def run_gpg(args, input_data=None):
    cmd = ["gpg", "--batch"] + args

    step(f"Running: {' '.join(cmd)}")

    return subprocess.run(
        cmd,
        input=input_data,
        capture_output=True,
        text=True
    )


def file_exists(path):
    if not os.path.isfile(path):
        err(f"File not found: {path}")
        return False

    return True


def output_path(input_file, suffix, output=None):
    if output:
        return output

    return input_file + suffix

if __name__ == "__main__":
    main()
