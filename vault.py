# ----------- Import necessary libraries -------------
import hashlib                   # For hashing the master password
from getpass import getpass      # For secure password input (no echo)
from time import sleep           # For adding delay between wrong attempts
from datetime import datetime    # For timestamp management
import os                        # For file existence and removal
import encrypt_decrypt
# ----------- Hashing function for master password -------------
def hash_passcode(password):
  return hashlib.blake2b(password.encode()).hexdigest()

# ----------- Create and write master password hash to file -------------
def create_hash_file(passcode, filename="master.hash"):
  with open(filename, "w") as f:
    f.write(passcode)

# ----------- Create an empty password storage file -------------
def create_passcode_file(filename="passcode.json"):
  with open(filename, "w") as f:
    f.write("{}")  # Initialize with empty dictionary

# ----------- Create a cooldown file with current time -------------
def create_cooldown_file(filename="cooldown.txt"):
  with open(filename, "w") as f:
    f.write(datetime.now().isoformat())  # Save time in ISO format

# ----------- Check if cooldown is still active -------------
def cooldown_time_checker():
  with open("cooldown.txt", "r") as f:
     cooldown_str = f.read()
  cooldown_time = datetime.fromisoformat(cooldown_str)  # Convert back to datetime object
  diff = datetime.now() - cooldown_time  # Time difference since last lock
  if diff.total_seconds() < 180:  # If less than 3 minutes passed
     remaining = 180 - diff.total_seconds()
     print(f"⏳ Wait {remaining/60:.1f} minutes")
     return False
  else:
     os.remove("cooldown.txt")  # Cooldown over, delete file
     return True

# ----------- Main Logic Starts Here -------------

# If no master hash exists, ask user to create one
if not os.path.exists("master.hash"):
   master_code = hash_passcode(getpass("Enter the master passcode :- \n"))
   create_hash_file(master_code)
   print("✅ Master password got saved")

else:
  # If password storage doesn't exist, create it
  if not os.path.exists("passcode.json"):
    create_passcode_file()
    print("📂 Created empty passcode file\n")

  else:
    # Check if cooldown file exists, and if cooldown is active
    if os.path.exists("cooldown.txt"):
      if not cooldown_time_checker():
        exit()  # Exit if still in cooldown
    
    # Give user 3 chances to input the correct master password
    for i in range(2, -1, -1):
      user_input = getpass("Enter the master passcode to access the passcode files \n")

      # If password is correct
      if open("master.hash", "r").read() == hash_passcode(user_input):
         print("✅ Access granted")
      
         action_to_do = input(
          "Choose an action to perform:\n"
          "1. Add password\n"
          "2. Read password\n"
          "3. Update password\n"
          "4. Delete password\n"
          "> "
            )
               
         match action_to_do:
            case "1":
              encrypt_decrypt.add_password()
            case "2":
               encrypt_decrypt.read_password()
            case "3":
               encrypt_decrypt.update_password()
            case "4":
               encrypt_decrypt.delete_password()
            case _:
             print("❌ Invalid option. Please choose from 1 to 4.")

             
      else:
        # If last try failed
        if i == 0:
            print("❌ All tries exhausted. Access denied.")
            create_cooldown_file()
            print("⏳ You can try again after 3 minutes")
        else:
            # Inform user of remaining tries
            print(f"❌ Wrong password. You have {i} tries left.")
            sleep(2)  # Wait before next attempt
