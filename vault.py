# ----------- Import necessary libraries -------------
import hashlib                   # For hashing the master password
from getpass import getpass      # For secure password input (no echo)
from time import sleep           # For adding delay between wrong attempts
from datetime import datetime    # For timestamp management
import os                        # For file existence and removal
import encry_decry         # Module containing encryption/decryption functions
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
import pwinput
# ----------- Hashing Function -------------
def master_password_to_key(password):
    """
    Hashes the master password using BLAKE2b hashing algorithm.

    Args:
        password (str): Plaintext master password.

    Returns:
        str: Hexadecimal hash of the password.
    """
    salt = encry_decry.get_salt()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))

    return key


# ----------- Save Hash to File -------------
def create_hash_file(passcode, filename="master.hash"):
    """
    Saves the hashed master password to a file.

    Args:
        passcode (str): Hashed master password.
        filename (str): File to store the hash.
    """
    with open(filename, "w") as f:
        f.write( hashlib.blake2b(passcode).hexdigest())


# ----------- Create Cooldown Timestamp -------------'

def create_cooldown_file(filename="cooldown.txt"):
    """
    Creates a cooldown file storing the current timestamp.
    Used to prevent brute-force attempts.
    """
    with open(filename, "w") as f:
        f.write(datetime.now().isoformat())


# ----------- Check if Cooldown is Active -------------
def cooldown_time_checker():
    """
    Checks if the cooldown period is still active.

    Returns:
        bool: True if cooldown has passed, False otherwise.
    """
    with open("cooldown.txt", "r") as f:
        cooldown_str = f.read()
    cooldown_time = datetime.fromisoformat(cooldown_str)
    diff = datetime.now() - cooldown_time

    if diff.total_seconds() < 180:
        remaining = 180 - diff.total_seconds()
        print(f"⏳ Wait {remaining / 60:.1f} minutes before retrying.")
        return False
    else:
        os.remove("cooldown.txt")
        return True


# ----------- Main Execution Starts Here -------------

if not os.path.exists("master.hash"):
    # If no master password exists, ask user to create one
    master_code = master_password_to_key (pwinput.pwinput(prompt= '🔐 Set a master passcode : ' , mask='*'))

    create_hash_file(master_code)
    print("✅ Master password saved securely.")

else:
    if os.path.exists("cooldown.txt"):
        if not cooldown_time_checker():
            exit()

    for i in range(2, -1, -1):
        entered_key = master_password_to_key(pwinput.pwinput(prompt= '🔐 Enter your master passcode :  ' , mask='*'))
        entered_key_hash = hashlib.blake2b(entered_key).hexdigest()

        with open("master.hash", "r") as f:
            stored_hash = f.read().strip()

        if entered_key_hash == stored_hash:
            print("✅ Access granted.")
            fernet = Fernet(entered_key)  # This is your final Fernet key

            action_to_do = input(
                "\nChoose an action to perform:\n"
                "1. Add password\n"
                "2. Read password\n"
                "3. Update password\n"
                "4. Delete password\n"
                "5. EXIT MENU\n> "
            )

            match action_to_do:
                case "1":
                    encry_decry.add_password(fernet)
                case "2":
                    encry_decry.read_password(fernet)
                case "3":
                    encry_decry.update_password(fernet)
                case "4":
                    encry_decry.delete_password(fernet)
                case "5":
                    exit()
                case _:
                    print("❌ Invalid option. Please choose a number between 1 to 5.")
            break
        
        else:
            if i == 0:
                print("❌ All attempts failed. Access denied.")
                create_cooldown_file()
                print("⏳ Try again after 3 minutes.")
            else:
                print(f"❌ Incorrect password. {i} attempt(s) left.")
                sleep(2)
