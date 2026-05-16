# 🔐 GPG File Encryption Tool

> A powerful, terminal-based CLI utility for encrypting, decrypting, signing, and verifying files using **GNU Privacy Guard (GPG)** — built for the Information Security final project at AUCA.

---

## 📌 Table of Contents

- [Problem Statement](#-problem-statement)
- [Solution Overview](#-solution-overview)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Features](#-features)
- [Setup & Installation](#-setup--installation)
- [Usage Guide](#-usage-guide)
- [Screenshots](#-screenshots)
- [Demo Video](#-demo-video)
- [Faculty Feedback](#-faculty-feedback)
- [Author](#-author)

---

## 🧩 Problem Statement

In today's digital environment, sensitive files — documents, credentials, reports — are routinely transmitted over insecure channels or stored without protection. Most encryption tools either require a graphical interface (inaccessible on servers) or demand deep cryptographic knowledge from the user.

**The challenge:** How can a developer or system administrator encrypt files quickly and correctly, entirely from the terminal, without needing to remember complex GPG flags?

---

## ✅ Solution Overview

`gpg_tool.py` is a **Python-based CLI wrapper** around GPG that provides a clean, guided interface for:

- **Symmetric encryption** — protect files with a passphrase (AES-256 by default)
- **Asymmetric encryption** — encrypt for a recipient using their public key
- **Digital signing** — create detached signatures to prove file authenticity
- **Signature verification** — detect tampering or verify the sender
- **Key management** — generate, list, and manage GPG key pairs

The tool adds colored output, clear error messages, file size reporting, and interactive prompts — making GPG accessible without sacrificing power.

---

## 🏗️ Architecture

```
gpg_tool.py
│
├── CLI Layer (argparse)
│   ├── encrypt    → Symmetric (AES-256) or Asymmetric (RSA) encryption
│   ├── decrypt    → Passphrase or private key decryption
│   ├── keygen     → Interactive or batch RSA key generation
│   ├── list-keys  → Display public and secret keys
│   ├── sign       → Detached signature creation
│   └── verify     → Signature verification
│
├── GPG Subprocess Layer
│   └── Calls gpg binary with safe, sanitized arguments
│
└── Output Layer
    ├── Colored terminal feedback (ANSI codes)
    ├── File size reporting
    └── Structured error messages
```

**Data Flow — Symmetric Encryption:**

```
User Input (file + passphrase)
        ↓
  gpg_tool.py (Python CLI)
        ↓
  GPG binary (subprocess)
        ↓
  AES-256 encrypted .gpg file  ← output
```

**Data Flow — Asymmetric Encryption:**

```
User Input (file + recipient email)
        ↓
  gpg_tool.py looks up recipient's public key
        ↓
  GPG encrypts with RSA public key
        ↓
  Only recipient's private key can decrypt
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.x |
| Crypto Backend | GnuPG (GPG 2.x) |
| CLI Parsing | Python `argparse` |
| Subprocess | Python `subprocess` |
| Output | ANSI terminal colors |
| Key Algorithm | RSA-4096 |
| Cipher | AES-256 (symmetric default) |

---

## ✨ Features

- 🔒 **Symmetric encryption** — AES-256 with passphrase (default)
- 🗝️ **Asymmetric encryption** — Encrypt for specific recipient by email or key ID
- ✍️ **File signing** — Detached `.sig` files for authenticity
- 🔍 **Signature verification** — Detect tampering
- 🧑‍💻 **Key generation** — Interactive or fully automated batch mode
- 📋 **Key listing** — View all public and secret keys in keyring
- 🎨 **Colored output** — Clear visual feedback with status icons
- 📏 **File size reporting** — See original vs encrypted size
- ⚡ **Safe passphrase handling** — Interactive prompt with confirmation

---

## ⚙️ Setup & Installation

### Prerequisites

```bash
# Debian / Ubuntu
sudo apt update && sudo apt install gnupg python3

# macOS
brew install gnupg python3

# Verify
gpg --version
python3 --version
```

### Clone the repository

```bash
git clone https://github.com/<your-username>/gpg-file-encryption-tool.git
cd gpg-file-encryption-tool
```

No external Python packages are required — only the Python standard library.

---

## 📖 Usage Guide

### 1. Encrypt a file (symmetric — passphrase)

```bash
python3 gpg_tool.py encrypt secret.pdf
# → Prompts for passphrase, outputs secret.pdf.gpg
```

With explicit passphrase (for scripting):
```bash
python3 gpg_tool.py encrypt secret.pdf --passphrase "StrongPass123!"
```

### 2. Encrypt for a recipient (asymmetric)

```bash
python3 gpg_tool.py encrypt report.pdf --recipient alice@example.com
```

The recipient must have their public key in your keyring.

### 3. Decrypt a file

```bash
python3 gpg_tool.py decrypt secret.pdf.gpg
# → Decrypts to secret.pdf (interactive passphrase prompt)
```

```bash
python3 gpg_tool.py decrypt secret.pdf.gpg --passphrase "StrongPass123!" --output restored.pdf
```

### 4. Generate a key pair

Interactive (recommended):
```bash
python3 gpg_tool.py keygen
```

Batch/automated:
```bash
python3 gpg_tool.py keygen --batch \
  --name "Alice Smith" \
  --email alice@auca.kg \
  --keysize 4096 \
  --expire 1y
```

### 5. List all keys

```bash
python3 gpg_tool.py list-keys
```

### 6. Sign a file

```bash
python3 gpg_tool.py sign report.pdf
# → Creates report.pdf.sig
```

### 7. Verify a signature

```bash
python3 gpg_tool.py verify report.pdf --sig report.pdf.sig
```

## 🎬 Demo Video

📺 **Watch the demo:** 

---

## 👤 Author

**ADILET TOLOSHOV**  
American University of Central Asia (AUCA)  
Information Security — Final Project  
Spring 2026

---

## 📄 License

This project is for educational purposes. GPG/GnuPG is licensed under the GPL.
