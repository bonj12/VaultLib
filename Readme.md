<div align="center">
  <img src="logo.png" alt="NeoVault Logo" width="300"/>

  # 🛡️ VaultLib (NeoVault)
  **🔒 Secure AES-256 vault hidden in images using EOF steganography.**

  [![Python Versions](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
  [![Arch Linux](https://img.shields.io/badge/OS-Arch_Linux-1793d1?style=flat-square&logo=arch-linux&logoColor=white)](https://archlinux.org/)
  [![Windows](https://img.shields.io/badge/OS-Windows-0078D6?style=flat-square&logo=windows&logoColor=white)](https://www.microsoft.com/windows)
  [![macOS](https://img.shields.io/badge/OS-macOS-000000?style=flat-square&logo=apple&logoColor=white)](https://www.apple.com/macos/)
  [![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey?style=flat-square)](https://creativecommons.org/licenses/by-nc/4.0/)
  [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
  [![GitHub stars](https://img.shields.io/github/stars/UndefinedClear/VaultLib?style=flat-square&color=yellow)](https://github.com/UndefinedClear/VaultLib/stargazers)
</div>

---

**VaultLib** is a professional-grade security tool designed to embed encrypted credential databases within standard image files. By leveraging **AES-256 (Fernet) encryption** and **EOF Steganography**, it ensures that sensitive data remains hidden in plain sight, maintaining the visual integrity of the carrier file. Perfect for those who value privacy and the "hidden in plain sight" philosophy.

## 📑 Table of Contents
- [✨ Key Features](#-key-features)
- [⚙️ Technical Overview](#️-technical-overview)
- [🚀 Getting Started](#-getting-started)
- [🏝️ Demo](#️-demo)
- [✍️ Usage Example](#️-usage-example)
- [📚 API Reference](#-api-reference)
- [📊 Analytics & Metrics](#-analytics--metrics)

---

## ✨ Key Features

* 👻 **Invisible Storage**: Implements EOF (End-of-File) steganography, allowing data to be stored behind valid image headers (JPG/PNG). The container file remains a perfectly viewable image.
* 🔒 **Military-Grade Encryption**: Utilizes AES-256 via the `cryptography` library with PBKDF2HMAC key derivation (200,000 iterations for robust key stretching).
* 🔑 **Custom Signatures**: Dynamic byte-marker injection (`NEO_SPACE_MARKER`) for reliable data offset identification, ensuring data integrity.
* 🎭 **Visual Camouflage**: Supports automated decoy display using system-native handlers (e.g., `xdg-open` on Linux), distracting casual observers.
* 🐧 **Arch-Friendly**: Designed with minimalism and control in mind, resonating with the Arch Linux philosophy.
* 🌐 **Session Management**: Integrated identity headers (`user`, `os`, `vault_name`) for multi-user or multi-environment vault deployments.

## ⚙️ Technical Overview

### Data Injection Workflow

The library appends a proprietary data block to the image binary after the standard end-of-file markers (`IEND` for PNG, `EOI` for JPG). This ensures the visual integrity of the host image is preserved.

```text
[ Original Image Binary ]
    (e.g., PNG header, IHDR, IDAT chunks, IEND marker)
+-------------------------+
|    NEO_SPACE_MARKER     |  <-- Custom byte signature to locate the payload
+-------------------------+
|          SALT           |  <-- 16-byte random salt for PBKDF2HMAC
+-------------------------+
|    ENCRYPTED_PAYLOAD    |  <-- Fernet-encrypted JSON (credentials data)
+-------------------------+