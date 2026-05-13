#!/usr/bin/env python3

import argparse
import subprocess
import sys
import os
import getpass
import shutil
from pathlib import Path


class Colors:
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    BOLD    = "\033[1m"
    RESET   = "\033[0m"


def ok(msg):
    print(f"{Colors.GREEN}[✓]{Colors.RESET} {msg}")


def err(msg):
    print(f"{Colors.RED}[✗]{Colors.RESET} {msg}", file=sys.stderr)


def info(msg):
    print(f"{Colors.CYAN}[i]{Colors.RESET} {msg}")


def warn(msg):
    print(f"{Colors.YELLOW}[!]{Colors.RESET} {msg}")


def step(msg):
    print(f"{Colors.BLUE}[→]{Colors.RESET} {msg}")


def banner():
    print(f"""
{Colors.BOLD}{Colors.CYAN}╔══════════════════════════════════════════════╗
║        GPG File Encryption Tool v1.0         ║
║      Information Security Final Project      ║
╚══════════════════════════════════════════════╝{Colors.RESET}
""")


def main():
    banner()


if __name__ == "__main__":
    main()
