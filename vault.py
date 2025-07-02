import hashlib
from getpass import getpass
from time import sleep
from datetime import datetime

import os


def hash_passcode(password):
  return hashlib.blake2b(password.encode()).hexdigest()

def create_hash_file(passcode , filename="master.hash"):
  with open(filename, "w") as f:
    f.write(passcode)

def create_passcode_file(filename ="passcode.json") :
  with open(filename, "w") as f:
    f.write("{}")

def create_cooldown_file(filename = "cooldown.txt") :
  with open(filename,"w")as f:
    f.write(datetime.now().isoformat())

def cooldown_time_checker() :
  with open("cooldown.txt", "r") as f:
     cooldown_str = f.read()
  cooldown_time = datetime.fromisoformat( cooldown_str)
  diff = datetime.now() - cooldown_time
  if diff.total_seconds() < 180:
     remaining = 180 - diff.total_seconds()
     print(f"⏳ Wait {remaining/60:.1f} minutes")
  else :
     os.remove("cooldown.txt")
     return True



if not os.path.exists("master.hash") :
   master_code = hash_passcode(getpass(" Enter the master passcode :- \n "))   
   create_hash_file(master_code)
   print("Master password got saved")

else:
 if not os.path.exists("passcode.json") :
  create_passcode_file()
  print("created empty passcoded file\n")

 else:
    if os.path.exists("cooldown.txt"):
      if not cooldown_time_checker():  # If it's still in cooldown
       exit()
    
    for i in range(2, -1, -1):
     user_input=getpass("Enter the master passcode to acess the passcode files \n")

     if open("master.hash", "r").read() == hash_passcode(user_input):
        print("✅ Access granted")
        break
     else:
        if i == 0:
            print("❌ All tries exhausted. Access denied.")
            create_cooldown_file()
            print("You can try later after 3 min")
        else:
            print(f"❌ Wrong password. You have {i} tries left.")
            sleep(2)  # adds delay before next attempt
