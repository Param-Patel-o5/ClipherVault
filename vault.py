# ----------- Import necessary libraries -------------
import hashlib                   # For hashing the master password
from getpass import getpass      # For secure password input (no echo)
from time import sleep           # For adding delay between wrong attempts
from datetime import datetime    # For timestamp management
import os                        # For file existence and removal
import encry_decry          # Module containing encryption/decryption functions


# ----------- Hashing Function -------------
def hash_passcode(password):
    """
    Hashes the master password using BLAKE2b hashing algorithm.

    Args:
        password (str): Plaintext master password.

    Returns:
        str: Hexadecimal hash of the password.
    """
    return hashlib.blake2b(password.encode()).hexdigest()


# ----------- Save Hash to File -------------
def create_hash_file(passcode, filename="master.hash"):
    """
    Saves the hashed master password to a file.

    Args:
        passcode (str): Hashed master password.
        filename (str): File to store the hash.
    """
    with open(filename, "w") as f:
        f.write(passcode)


# ----------- Create Cooldown Timestamp -------------
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
    master_code = hash_passcode(getpass("🔐 Set a master passcode: "))
    create_hash_file(master_code)
    print("✅ Master password saved securely.")

else:
    # If cooldown file exists, check if cooldown is active
    if os.path.exists("cooldown.txt"):
        if not cooldown_time_checker():
            exit()

    # Allow 3 attempts to enter correct password
    for i in range(2, -1, -1):
        user_input = getpass("🔐 Enter master passcode to access the vault: ")

        if open("master.hash", "r").read() == hash_passcode(user_input):
            print("✅ Access granted.")
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
                    encry_decry.add_password()
                case "2":
                    encry_decry.read_password()
                case "3":
                    encry_decry.update_password()
                case "4":
                    encry_decry.delete_password()
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
                sleep(2)  # Delay before next attempt
