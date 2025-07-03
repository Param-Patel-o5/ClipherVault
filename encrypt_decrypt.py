import json                   # For reading/writing passcode data in JSON format
import base64                 # For encoding the derived key
import os                     # For checking if salt or vault file exists
import getpass                # For secure input (hides input)
from cryptography.fernet import Fernet     # For encryption and decryption
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC  # Key derivation
from cryptography.hazmat.primitives import hashes     # Hashing algorithm
from cryptography.hazmat.backends import default_backend  # Cryptography backend

# ---------- CONFIG ----------
VAULT_FILE = "passcode.json"     # Main vault to store encrypted passwords
SALT_FILE = "salt.salt"          # File to store randomly generated salt

# ---------- Generate or Load Salt ----------
def get_salt():
    if not os.path.exists(SALT_FILE):      # If salt file doesn't exist
        salt = os.urandom(16)              # Generate new random 16-byte salt
        with open(SALT_FILE, "wb") as f:   # Save salt to file
            f.write(salt)
    else:
        with open(SALT_FILE, "rb") as f:   # Load existing salt
            salt = f.read()
    return salt                            # Return salt value

# ---------- Derive Fernet Key from Master Password ----------
def load_fernet(master_password):
    salt = get_salt()                      # Load salt (or generate it)

    # Set up the key derivation function with salt + master password
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),         # Use SHA-256 as hash function
        length=32,                         # Output length = 32 bytes
        salt=salt,                         # Salt for extra randomness
        iterations=100_000,                # Number of iterations = more secure
        backend=default_backend()          # Use default backend
    )

    # Derive encryption key from password and encode to make Fernet-compatible
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return Fernet(key)                    # Return Fernet object

# ---------- Placeholder Functions ----------
def add_password():
    print("🔐 Add password function not yet implemented")

def read_password():
    print("📖 Read password function not yet implemented")

def update_password():
    print("✏️ Update password function not yet implemented")

def delete_password():
    print("❌ Delete password function not yet implemented")
