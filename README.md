# 🔐 ClipherVault – A Simple Yet Secure Password Manager

ClipherVault is a **command-line password manager** built in Python, designed for those who want secure credential storage with zero third-party dependencies (except `cryptography`).  
It encrypts your data locally using your **master password**, and supports basic password operations like **add, read, update, delete** — all protected behind a hash-verified login system and encrypted vault.

---

## 🚀 Features

- ✅ **Master password protection** (with BLAKE2b hashing)
- ✅ **Encrypted vault** using `Fernet` + derived key from `PBKDF2HMAC`
- ✅ **Add, read, update, and delete credentials**
- ✅ **Brute-force protection** — 3 failed attempts lock the app for 3 minutes
- ✅ **Auto vault creation** if files don’t exist
- ✅ **Separate encryption and interface logic** (modular structure)
- ✅ Clean console interface using `getpass()` (for secure input)

---

## 🛠️ How Encryption Works

We use:

- **PBKDF2HMAC** from `cryptography` to derive a key from the master password
- **Fernet symmetric encryption** to encrypt/decrypt your password entries
- **A unique `salt.salt` file** ensures each user's key is unique even for the same master password
- **BLAKE2b** (via `hashlib`) to securely store the master password hash

This ensures that:

- Vault data is **never stored in plaintext**
- The app doesn’t rely on insecure password matching
- Even the derived encryption key is not saved anywhere — it’s generated fresh each time

---

## 💻 Skills Demonstrated

| Area | What You Used |
|------|----------------|
| Python | `getpass`, `hashlib`, `json`, `os`, `time`, `datetime`, `input-handling` |
| Security | `cryptography.fernet`, `PBKDF2HMAC`, `BLAKE2b`, key derivation, salt |
| Logic | CLI-driven menu, user auth, cooldown logic |
| Design | Modular codebase (separating encryption & logic) |
| Git | GitHub repo management, README writing |

---

## 🧪 How to Run

1. **Clone the repo**
   ```bash
   git clone https://github.com/Param-Patel-o5/ClipherVault.git
   cd ClipherVault
   ```

2. **Install dependencies**
   ```bash
   pip install cryptography
   ```

3. **Run the app**
   ```bash
   python vault.py
   ```

4. **Follow the CLI prompts to set your master password and manage credentials.**

---

## 👀 Sneak Peek (Coming Soon)

We'll add a simple **Tkinter-based GUI** that allows you to:
- Enter passwords via a form
- View stored entries in a table
- Copy credentials to clipboard securely
- Auto-generate random passwords

---

## 🧠 Future Plans

- [x] Finish CLI version ✅
- [ ] Add GUI using Tkinter
- [ ] Add password generator using `secrets` library


---

## 🤝 Contribution

Pull requests are welcome!  
Please open an issue first to discuss what you would like to change.

---

## 📝 License

This project is open-source under the [MIT License](LICENSE).

---

## ✨ Author

Made with ❤️ by [Param-Patel-o5](https://github.com/Param-Patel-o5)

