import json
import base64
import os
import hashlib
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
    """
    Returns the salt value used for key derivation.
    If the salt file does not exist, creates a new salt and saves it.
    """
    if not os.path.exists(SALT_FILE):
        salt = os.urandom(16)
        with open(SALT_FILE, "wb") as f:
            f.write(salt)
    else:
        with open(SALT_FILE, "rb") as f:
            salt = f.read()
    return salt


# ---------- Load Vault Data ----------
def load_vault_data():
    """
    Loads and returns the content of the vault file (passcode.json).
    Returns an empty dictionary if the file does not exist or is empty.
    """
    if os.path.exists(VAULT_FILE) and os.path.getsize(VAULT_FILE) > 0:
        with open(VAULT_FILE, "r") as f:
            return json.load(f)
    return {}


# ---------- Derive Fernet Key ----------
def load_fernet(master_password):
    """
    Derives a Fernet encryption key from the master password using PBKDF2HMAC and salt.

    Args:
        master_password (str): The user's master password.

    Returns:
        Fernet: A Fernet object initialized with the derived key.
    """
    salt = get_salt()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return Fernet(key)


# ---------- Add Password ----------
def add_password():
    """
    Prompts the user for a site and password, encrypts it, and saves it to the vault.
    """
    fernet = load_fernet(getpass("Enter your master password again: "))
    site_name = input("🌐 Enter the site/username: ")
    encrypted_password = fernet.encrypt(
        getpass("🔑 Enter the password you want to save: ").encode()
    ).decode()

    data = load_vault_data()
    data[site_name] = encrypted_password

    with open(VAULT_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print("✅ Password saved successfully.")


# ---------- Read Password ----------
def read_password():
    """
    Prompts the user for a site name, decrypts the stored password, and displays it.
    """
    fernet = load_fernet(getpass("Enter your master password again: "))
    site_name = input("🌐 Enter the site/username you want the password for: ")

    data = load_vault_data()

    if not data:
        print("⚠️ No saved passwords yet.")
        return

    if site_name in data:
        encrypted = data[site_name].encode()
        decrypted = fernet.decrypt(encrypted).decode()
        print(f"🔓 Password for '{site_name}': {decrypted}")
    else:
        print("⚠️ Site not found.")


# ---------- Update Password ----------
def update_password():
    """
    Updates an existing password or adds a new one after confirmation from the user.
    """
    fernet = load_fernet(getpass("Enter your master password again: "))
    site_name = input("🌐 Enter the site/username you want to update the password for: ")
    encrypted_password = fernet.encrypt(
        getpass("🔑 Enter the new password: ").encode()
    ).decode()

    data = load_vault_data()

    is_new = False
    if site_name not in data:
        confirm = input(f"⚠️ '{site_name}' does not exist. Save as new? (y/n): ").lower()
        if confirm != 'y':
            print("❌ Cancelled. No changes made.")
            return
        is_new = True

    data[site_name] = encrypted_password

    with open(VAULT_FILE, "w") as f:
        json.dump(data, f, indent=4)

    if is_new:
        print("✅ New password added successfully.")
    else:
        print("✅ Password updated successfully.")

def hash_passcode(password):
    """
    Hashes the master password using BLAKE2b hashing algorithm.

    Args:
        password (str): Plaintext master password.

    Returns:
        str: Hexadecimal hash of the password.
    """
    return hashlib.blake2b(password.encode()).hexdigest()

# ---------- Delete Password ----------
def delete_password():
    """
    Deletes a stored password entry after verifying the master password.
    """
    master_input = getpass("Enter your master password again: ")
    with open("master.hash", "r") as f:
        stored_hash = f.read()

    if hash_passcode(master_input) != stored_hash:
        print("❌ Incorrect master password. Access denied.")
        return

    site_name = input("🌐 Enter the site/username you want to delete from the list: ")
    data = load_vault_data()

    if not data:
        print("⚠️ No saved passwords yet.")
        return

    if site_name in data:
        del data[site_name]
        with open(VAULT_FILE, "w") as f:
            json.dump(data, f, indent=4)
        print("✅ Password deleted successfully.")
    else:
        print("⚠️ Site not found.")
