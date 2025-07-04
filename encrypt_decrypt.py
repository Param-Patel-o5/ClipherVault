import json
import base64
import os
from getpass import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# ---------- CONFIG ----------
VAULT_FILE = "passcode.json"     # File to store all encrypted passwords
SALT_FILE = "salt.salt"          # File to store the salt (important for key derivation)

# ---------- Generate or Load Salt ----------
def get_salt():
    """Returns the salt value used for key derivation. Creates one if not present."""
    if not os.path.exists(SALT_FILE):
        salt = os.urandom(16)
        with open(SALT_FILE, "wb") as f:
            f.write(salt)
    else:
        with open(SALT_FILE, "rb") as f:
            salt = f.read()
    return salt

# ---------- Derive a Fernet Key from Master Password ----------
def load_fernet(master_password):
    """
    Derives a Fernet encryption key from the master password using PBKDF2HMAC and salt.
    """
    salt = get_salt()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),    # Secure hashing algorithm
        length=32,                    # Fernet requires 32-byte keys
        salt=salt,
        iterations=100_000,           # High iteration count for brute-force resistance
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return Fernet(key)

# ---------- Add Password ----------
def add_password():
    """Encrypts and saves a new password for a given site or service."""
    fernet = load_fernet(getpass("Enter your master password again: "))
    site_name = input("🌐 Enter the site/username: ")
    encrypted_password = fernet.encrypt(
        getpass("🔑 Enter the password you want to save: ").encode()
    ).decode()

    # Load existing data
    if os.path.exists(VAULT_FILE) and os.path.getsize(VAULT_FILE) > 0:
        with open(VAULT_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}

    # Add new password
    data[site_name] = encrypted_password

    # Save updated dictionary
    with open(VAULT_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print("✅ Password saved successfully.")

# ---------- Read Password ----------
def read_password():
    """Decrypts and displays a password for a given site/username."""
    fernet = load_fernet(getpass("Enter your master password again: "))
    site_name = input("🌐 Enter the site/username you want the password for: ")

    if os.path.exists(VAULT_FILE) and os.path.getsize(VAULT_FILE) > 0:
        with open(VAULT_FILE, "r") as f:
            data = json.load(f)

        if site_name in data:
            encrypted = data[site_name].encode()
            decrypted = fernet.decrypt(encrypted).decode()
            print(f"🔓 Password for '{site_name}': {decrypted}")
        else:
            print("⚠️ Site not found.")
    else:
        print("⚠️ No saved passwords yet.")

# ---------- Update Password ----------
def update_password():
    """Updates an existing password, or optionally adds a new one."""
    fernet = load_fernet(getpass("Enter your master password again: "))
    site_name = input("🌐 Enter the site/username you want to update the password for: ")
    encrypted_password = fernet.encrypt(
        getpass("🔑 Enter the new password: ").encode()
    ).decode()

    # Load existing data
    if os.path.exists(VAULT_FILE) and os.path.getsize(VAULT_FILE) > 0:
        with open(VAULT_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}

    # Ask to add if site doesn't exist
    is_new = False
    if site_name not in data:
        confirm = input(f"⚠️ '{site_name}' does not exist. Save as new? (y/n): ").lower()
        if confirm != 'y':
            print("❌ Cancelled. No changes made.")
            return
        is_new = True

    # Save/update
    data[site_name] = encrypted_password
    with open(VAULT_FILE, "w") as f:
        json.dump(data, f, indent=4)

    if is_new:
        print("✅ New password added successfully.")
    else:
        print("✅ Password updated successfully.")

# ---------- Delete Password (TODO) ----------
def delete_password():
    """Placeholder for deleting a password entry."""
    print("❌ Delete password function not yet implemented.")
