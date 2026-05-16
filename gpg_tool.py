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
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


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


def check_gpg():
    if not shutil.which("gpg"):
        err("GPG is not installed or not in PATH.")
        sys.exit(1)


def run_gpg(args: list, input_data: str = None) -> subprocess.CompletedProcess:
    cmd = ["gpg", "--batch"] + args

    step(f"Running: {' '.join(cmd)}")

    result = subprocess.run(
        cmd,
        input=input_data,
        capture_output=True,
        text=True
    )

    return result


def file_exists(path: str) -> bool:
    if not os.path.isfile(path):
        err(f"File not found: {path}")
        return False

    return True


def output_path(input_file: str, suffix: str, output: str = None) -> str:
    if output:
        return output

    return input_file + suffix


def cmd_encrypt(args):
    if not file_exists(args.file):
        return 1

    info(f"Encrypting: {args.file}")

    gpg_args = ["--yes", "--armor"]

    if args.recipient:
        info(f"Mode: Asymmetric ({args.recipient})")

        gpg_args += [
            "--encrypt",
            "--recipient",
            args.recipient
        ]

        if args.sign:
            gpg_args += ["--sign"]
    else:
        info("Mode: Symmetric")

        if args.passphrase:
            passphrase = args.passphrase
        else:
            passphrase = getpass.getpass("Enter passphrase: ")
            confirm = getpass.getpass("Confirm passphrase: ")

            if passphrase != confirm:
                err("Passphrases do not match.")
                return 1

        gpg_args += [
            "--symmetric",
            "--cipher-algo",
            args.cipher,
            "--passphrase",
            passphrase
        ]

    out = output_path(args.file, ".gpg", args.output)

    gpg_args += [
        "--output",
        out,
        args.file
    ]

    result = run_gpg(gpg_args)

    if result.returncode == 0:
        ok(f"Encrypted → {out}")

        size_in = os.path.getsize(args.file)
        size_out = os.path.getsize(out)

        info(f"Original size : {size_in:,} bytes")
        info(f"Encrypted size: {size_out:,} bytes")

        return 0

    err("Encryption failed.")
    print(result.stderr, file=sys.stderr)

    return 1


def cmd_decrypt(args):
    if not file_exists(args.file):
        return 1

    info(f"Decrypting: {args.file}")

    out = args.output

    if not out:
        out = (
            args.file[:-4]
            if args.file.endswith(".gpg")
            else args.file + ".decrypted"
        )

    gpg_args = [
        "--yes",
        "--output",
        out
    ]

    if args.passphrase:
        gpg_args += [
            "--passphrase",
            args.passphrase
        ]
    else:
        gpg_args = [
            "gpg",
            "--yes",
            "--output",
            out,
            "--decrypt",
            args.file
        ]

        step(f"Running: {' '.join(gpg_args)}")

        result = subprocess.run(
            gpg_args,
            capture_output=False
        )

        if result.returncode == 0:
            ok(f"Decrypted → {out}")
            return 0

        err("Decryption failed.")
        return 1

    gpg_args += [
        "--decrypt",
        args.file
    ]

    result = run_gpg(gpg_args)

    if result.returncode == 0:
        ok(f"Decrypted → {out}")
        return 0

    err("Decryption failed.")
    print(result.stderr, file=sys.stderr)

    return 1


def cmd_keygen(args):
    info("Generating GPG key pair")

    if args.batch:
        name = args.name or "GPG Tool User"
        email = args.email or "user@example.com"
        expire = args.expire or "1y"
        passphrase = args.passphrase or ""

        batch_params = f"""
%echo Generating key
Key-Type: RSA
Key-Length: {args.keysize}
Subkey-Type: RSA
Subkey-Length: {args.keysize}
Name-Real: {name}
Name-Email: {email}
Expire-Date: {expire}
Passphrase: {passphrase}
%commit
%echo done
"""

        result = run_gpg(
            ["--gen-key", "--batch"],
            input_data=batch_params
        )

        if result.returncode == 0:
            ok(f"Key pair generated for {name} <{email}>")
            print(result.stderr)
        else:
            err("Key generation failed.")
            print(result.stderr, file=sys.stderr)
            return 1
    else:
        subprocess.run(["gpg", "--full-gen-key"])

    return 0


def cmd_list_keys(args):
    print(f"\n{Colors.BOLD}{Colors.CYAN}=== Public Keys ==={Colors.RESET}")

    subprocess.run([
        "gpg",
        "--list-keys",
        "--keyid-format",
        "LONG"
    ])

    print(f"\n{Colors.BOLD}{Colors.CYAN}=== Secret Keys ==={Colors.RESET}")

    subprocess.run([
        "gpg",
        "--list-secret-keys",
        "--keyid-format",
        "LONG"
    ])

    return 0


def cmd_sign(args):
    if not file_exists(args.file):
        return 1

    info(f"Signing: {args.file}")

    out = output_path(args.file, ".sig", args.output)

    gpg_args = [
        "--yes",
        "--armor",
        "--detach-sign",
        "--output",
        out
    ]

    if args.key:
        gpg_args += [
            "--local-user",
            args.key
        ]

    gpg_args += [args.file]

    result = subprocess.run(
        ["gpg"] + gpg_args,
        capture_output=False
    )

    if result.returncode == 0:
        ok(f"Signature saved → {out}")
    else:
        err("Signing failed.")

    return result.returncode


def cmd_verify(args):
    if not file_exists(args.file):
        return 1

    info(f"Verifying: {args.file}")

    if args.sig:
        result = subprocess.run([
            "gpg",
            "--verify",
            args.sig,
            args.file
        ])
    else:
        result = subprocess.run([
            "gpg",
            "--verify",
            args.file
        ])

    if result.returncode == 0:
        ok("Signature is VALID.")
    else:
        err("Signature is INVALID.")

    return result.returncode


def build_parser():
    parser = argparse.ArgumentParser(
        prog="gpg_tool",
        description="GPG encryption utility",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    sub = parser.add_subparsers(
        dest="command",
        metavar="COMMAND"
    )

    sub.required = True

    p_enc = sub.add_parser(
        "encrypt",
        help="Encrypt a file"
    )

    p_enc.add_argument(
        "file",
        help="File to encrypt"
    )

    p_enc.add_argument(
        "-o",
        "--output"
    )

    p_enc.add_argument(
        "-r",
        "--recipient"
    )

    p_enc.add_argument(
        "-p",
        "--passphrase"
    )

    p_enc.add_argument(
        "--cipher",
        default="AES256"
    )

    p_enc.add_argument(
        "--sign",
        action="store_true"
    )

    p_dec = sub.add_parser(
        "decrypt",
        help="Decrypt a file"
    )

    p_dec.add_argument("file")

    p_dec.add_argument(
        "-o",
        "--output"
    )

    p_dec.add_argument(
        "-p",
        "--passphrase"
    )

    p_kg = sub.add_parser(
        "keygen",
        help="Generate key pair"
    )

    p_kg.add_argument(
        "--batch",
        action="store_true"
    )

    p_kg.add_argument("--name")
    p_kg.add_argument("--email")
    p_kg.add_argument("--passphrase")

    p_kg.add_argument(
        "--keysize",
        type=int,
        default=4096
    )

    p_kg.add_argument(
        "--expire",
        default="1y"
    )

    sub.add_parser(
        "list-keys",
        help="List all keys"
    )

    p_sig = sub.add_parser(
        "sign",
        help="Sign a file"
    )

    p_sig.add_argument("file")

    p_sig.add_argument(
        "-o",
        "--output"
    )

    p_sig.add_argument(
        "-k",
        "--key"
    )

    p_ver = sub.add_parser(
        "verify",
        help="Verify signature"
    )

    p_ver.add_argument("file")

    p_ver.add_argument(
        "--sig"
    )

    return parser


def main():
    banner()

    check_gpg()

    parser = build_parser()

    args = parser.parse_args()

    dispatch = {
        "encrypt": cmd_encrypt,
        "decrypt": cmd_decrypt,
        "keygen": cmd_keygen,
        "list-keys": cmd_list_keys,
        "sign": cmd_sign,
        "verify": cmd_verify
    }

    handler = dispatch.get(args.command)

    if handler:
        sys.exit(handler(args))

    parser.print_help()
    sys.exit(1)


if __name__ == "__main__":
    main()
