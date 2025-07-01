import hashlib
from getpass import getpass
import os


def hash_passcode(password):
  return hashlib.blake2b(password.encode()).hexdigest()

def create_hash_file(passcode , filename="master.hash"):
  with open(filename, "w") as f:
    f.write(passcode)


if not os.path.exists("master.hash") :
   master_code = hash_passcode(getpass(" Enter the master passcode :- \n "))   
   create_hash_file(master_code)
   print("Master password got saved")

else:
 pass

