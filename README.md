# Password Manager

A command-line password vault built with Python and `cryptography`. Credentials are protected with a master password, a random salt, PBKDF2-HMAC-SHA256 key derivation, and Fernet authenticated encryption.

> **Security note:** This is an educational password-manager project, not a production replacement for an audited password manager. Do not use it to store critical real-world credentials without further security review.

## Features

- Master-password protected vault
- PBKDF2-HMAC-SHA256 key derivation with a per-vault random salt
- Fernet authenticated encryption for stored passwords
- Add, retrieve, list, and delete credentials
- Local JSON persistence
- Salt and vault data excluded from Git

## Tech Stack

- Python 3
- `cryptography`
- JSON file storage
- PBKDF2-HMAC-SHA256
- Fernet symmetric authenticated encryption

## Project Structure

```text
password-manager/
├── vault.py
├── encrypt_test.py
├── requirements.txt
└── .gitignore
```

## Run Locally

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python vault.py
```

On Linux/macOS, activate the environment with `source venv/bin/activate`.

The application creates local `vault_data.json` and `salt.bin` files. These files are intentionally ignored by Git.

## Security Design

The master password is not stored directly. A random salt is generated and PBKDF2-HMAC-SHA256 derives a 32-byte key. Fernet then encrypts credential passwords and provides authenticated decryption.

## Limitations / Next Steps

For production use, I would add a memory-hard KDF such as Argon2id, stronger input handling, clipboard support with secure clearing, structured logging without secrets, automated tests, lockout/rate limiting, and a security audit.
