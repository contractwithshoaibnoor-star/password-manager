import os
import json
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

VAULT_FILE = "vault_data.json"
SALT_FILE = "salt.bin"


def derive_key(master_password, salt):
    """Master password aur salt se ek Fernet-compatible key banata hai."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return key


class Vault:
    def __init__(self):
        self.entries = {}
        self.fernet = None

    def setup(self, master_password):
        salt = os.urandom(16)
        with open(SALT_FILE, "wb") as f:
            f.write(salt)

        key = derive_key(master_password, salt)
        self.fernet = Fernet(key)
        self.entries = {}
        self.save()
        print("Naya vault ban gaya master password ke saath.")

    def unlock(self, master_password):
        if not os.path.exists(SALT_FILE):
            print("Vault abhi tak banaya nahi gaya. Pehle setup() chalao.")
            return False

        with open(SALT_FILE, "rb") as f:
            salt = f.read()

        key = derive_key(master_password, salt)
        self.fernet = Fernet(key)

        return self.load()

    def add(self, site, username, password):
        encrypted_password = self.fernet.encrypt(password.encode()).decode()
        self.entries[site] = {
            "username": username,
            "password": encrypted_password
        }
        self.save()
        print(f"'{site}' add ho gaya vault mein.")

    def get(self, site):
        if site not in self.entries:
            print(f"'{site}' vault mein nahi mila.")
            return
        entry = self.entries[site]
        decrypted_password = self.fernet.decrypt(entry["password"].encode()).decode()
        print(f"Site: {site}")
        print(f"Username: {entry['username']}")
        print(f"Password: {decrypted_password}")

    def list_sites(self):
        if not self.entries:
            print("Vault khaali hai.")
            return
        print("Stored sites:")
        for site in self.entries:
            print(f"- {site}")

    def delete(self, site):
        if site in self.entries:
            del self.entries[site]
            self.save()
            print(f"'{site}' delete ho gaya.")
        else:
            print(f"'{site}' vault mein nahi mila.")

    def save(self):
        with open(VAULT_FILE, "w") as f:
            json.dump(self.entries, f)

    def load(self):
        if not os.path.exists(VAULT_FILE):
            self.entries = {}
            return True

        with open(VAULT_FILE, "r") as f:
            data = json.load(f)

        try:
            for site, entry in data.items():
                self.fernet.decrypt(entry["password"].encode())
            self.entries = data
            return True
        except Exception:
            print("Ghalat master password!")
            return False


def print_menu():
    print("\n===== Password Manager =====")
    print("1. Add credential")
    print("2. Get credential")
    print("3. List sites")
    print("4. Delete credential")
    print("5. Exit")


def main():
    vault = Vault()

    if not os.path.exists(SALT_FILE):
        pw = input("Naya master password banayein: ")
        vault.setup(pw)
    else:
        pw = input("Master password enter karein: ")
        if not vault.unlock(pw):
            return

    while True:
        print_menu()
        choice = input("Apna option chunein (1-5): ").strip()

        if choice == "1":
            site = input("Site ka naam: ").strip()
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            if not site or not username or not password:
                print("Koi bhi field khaali nahi honi chahiye.")
                continue
            vault.add(site, username, password)

        elif choice == "2":
            site = input("Kis site ka credential chahiye: ").strip()
            vault.get(site)

        elif choice == "3":
            vault.list_sites()

        elif choice == "4":
            site = input("Kis site ko delete karna hai: ").strip()
            vault.delete(site)

        elif choice == "5":
            print("Vault band ho raha hai. Alvida!")
            break

        else:
            print("Ghalat option, dobara try karein.")


if __name__ == "__main__":
    main()