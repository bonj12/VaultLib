# 🐱 NeoVault (VaultLib)

**A High-Security Steganographic Password Management Library for Python.**

`NeoVault` is a professional-grade security tool designed to embed encrypted credential databases within standard image files. By leveraging **AES-256 (Fernet) encryption** and **EOF Steganography**, it ensures that sensitive data remains hidden in plain sight, maintaining the visual integrity of the carrier file. Perfect for those who value privacy and the "hidden in plain sight" philosophy.

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

```
[ Original Image Binary ]
    (e.g., PNG header, IHDR, IDAT chunks, IEND marker)
+-------------------------+
|    NEO_SPACE_MARKER     |  <-- Your custom signature
+-------------------------+
|          SALT           |  <-- 16-byte random salt
+-------------------------+
|    ENCRYPTED_PAYLOAD    |  <-- Fernet-encrypted JSON (credentials)
+-------------------------+

```

## 🚀 Getting Started

### Installation

1. Create Venv for project (python 3.11)
    ```bash
    $ python3 -m venv venv
    ```

2. Activate venv<br>
    ## 🐟 Fish:

    ```bash
    $ source venv/bin/activate.fish
    ```

    ## 💫 Zsh and Bash:

    ```bash
    $ source venv/bin/activate
    ```

3. Ensure you have the `cryptography` library installed:

    ```bash
    $ pip install cryptography
    ```

4. 🏁 Thats All


### Prerequisites

* A Python environment (3.8+ recommended).

## 🏝️ Demo
### 🐈 Mask image (mask_cat.jpg)
![mask_cat.jpg](<mask_cat.jpg>)

### 🔒 Vault image (cat.png)
![cat.png](<cat.png>)

## ✍️ Usage Example

The following implementation demonstrates how to initialize a vault, manage entries, and retrieve a comprehensive list of stored services using `VaultLib`.

```python
import VaultLib as vl

# 1. Initialize the Vault 🛡️
# If 'cat.png' does not exist, it will be created using 'mask_cat.jpg'.
# The 'show_logo' option displays the Arch Linux ASCII art.
vault = vl.Vault(
    vault_name="MySecureVault", # (Not Neccessary)
    master_password="YourUltraStrongPassword123!", # ⚠️ USE A STRONG, UNIQUE PASSWORD!
    out_image="cat.png",                          # The output image containing encrypted data
    mask_source="mask_cat.jpg",                   # Mask image (If None it will be 1 pixel)
    user='Alex',                                  # Custom user identifier (Not Neccessary)
    os="Arch Linux",                              # Operating system for display (Not Neccessary)
    show_logo=True                                # Display ASCII logo on initialization (Not Neccessary)
)

# 2. Add New Credentials ➕
# A secure, random 20-character password will be generated automatically.
print("\n--- Adding New Entry ---")
generated_pass = vault.add_entry("GitHub", "alex_arch_user", length=24)
print(f"Generated password for GitHub: {generated_pass}")

# Add another entry
vault.add_entry("Spotify", "alex_music_lover")

# 3. List All Stored Services 📜
print("\n--- Listing All Services ---")
vault.list_entries()

# 4. Retrieve Specific Credentials 🔍
print("\n--- Retrieving Specific Entries ---")
services_list = vault.get_services() # Get a raw list of service names

if services_list:
    for service_name in services_list:
        status_code, data_entry = vault.get_entry(service_name)
        
        if status_code == 2:
            print(f"[✅ SUCCESS] Service: {service_name}")
            print(f"            Login:   {data_entry['login']}")
            print(f"            Password: {data_entry['password']}")
        elif status_code == 1:
            print(f"[❌ ERROR] Unauthorized: Invalid Master Password detected for '{service_name}'.")
        elif status_code == 0:
            print(f"[❓ INFO] Service '{service_name}' not found.")
else:
    print("[⚠️ WARNING] No services found or vault access denied.")

```

## 🔒 Security & Privacy

* **Robust Key Derivation**: Employs `PBKDF2HMAC` with `SHA256` and a high number of iterations (200,000) to significantly increase the computational cost of brute-force attacks on the master password.
* **Ephemeral Master Key**: The master password is never stored. It is used solely for key derivation during each session.
* **Integrity by Design**: The steganographic approach ensures that any casual inspection of the image file will reveal only the image itself, with no indication of hidden data.
* **Source Code Transparency**: Open-source nature allows for full auditing and verification of security practices.

## 📚 API Reference

| Method | Description | Return Type |
| --- | --- | --- |
| `__init__(...)` | Initializes the vault instance. | `None` |
| `add_entry(service, login, length)` | Generates and encrypts a new password for a given service and login. | `str` (the generated password) |
| `get_entry(service)` | Decrypts and retrieves specific service details. | `list [status_code, data_dict]` |
| `get_services()` | Returns a list of all stored service identifiers. | `list[str] | None` |
| `list_entries()` | Prints a formatted table of all services to the console. | `None` |

## 📊 Analytics & Metrics

### Download Trends

*Represents the monthly download activity for VaultLib.*

### Star History

*A graph showing the project's star growth over time.*

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## 📝 License

This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**. 

**You are free to:**
* Share and Adapt the code for personal use.

**Under the following terms:**
* **Attribution**: You must give appropriate credit.
* **Non-Commercial**: You may NOT use the material for commercial purposes.

[Read More](<LICENCE>)

---