import json
import os
import pwinput
from getpass import getpass
from cryptography.fernet import Fernet

# ---------- CONFIG ----------
VAULT_FILE = "passcode.json"     # File to store all encrypted passwords
SALT_FILE = "salt.salt"          # File to store the salt (for key derivation)


# ---------- Generate or Load Salt ----------
def get_salt() -> bytes:
    """
    Returns the salt value used for key derivation.
    If the salt file does not exist, creates a new salt and saves it.

    Returns:
        bytes: The salt value.
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
def load_vault_data() -> dict:
    """
    Loads and returns the content of the vault file (passcode.json).
    Returns an empty dictionary if the file does not exist or is empty.

    Returns:
        dict: Dictionary of stored site-password entries.
    """
    if os.path.exists(VAULT_FILE) and os.path.getsize(VAULT_FILE) > 0:
        with open(VAULT_FILE, "r") as f:
            return json.load(f)
    return {}


# ---------- Add Password ----------
def add_password(fernet: Fernet) -> None:
    """
    Prompts the user for a site and password, encrypts it, and saves it to the vault.

    Args:
        fernet (Fernet): The Fernet object for encryption.
    """
    site_name = input("🌐 Enter the site/username: ")
    password =  pwinput.pwinput(prompt= '🔑 Enter the password you want to save : ' , mask='*')

    encrypted_password = fernet.encrypt(password.encode()).decode()

    data = load_vault_data()
    data[site_name] = encrypted_password

    with open(VAULT_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print("✅ Password saved successfully.")


# ---------- Read Password ----------
def read_password(fernet: Fernet) -> None:
    """
    Prompts the user for a site name, decrypts the stored password, and displays it.

    Args:
        fernet (Fernet): The Fernet object for decryption.
    """
    site_name = input("🌐 Enter the site/username you want the password for : ")

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
def update_password(fernet: Fernet) -> None:
    """
    Updates an existing password or adds a new one after confirmation from the user.

    Args:
        fernet (Fernet): The Fernet object for encryption.
    """
    site_name = input("🌐 Enter the site/username you want to update the password for : ")
    new_password = pwinput.pwinput(prompt= '🔑 Enter the new password: ', mask='*')

    encrypted_password = fernet.encrypt(new_password.encode()).decode()

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


# ---------- Delete Password ----------
def delete_password() -> None:
    """
    Deletes a stored password entry.

    Args:
        fernet (Fernet): Not used here, included for consistency with other functions.
    """
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
