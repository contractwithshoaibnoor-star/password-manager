from cryptography.fernet import Fernet

key = Fernet.generate_key()
print("Generated Key:", key)

fernet = Fernet(key)

message = "MySecretPassword123"
encrypted = fernet.encrypt(message.encode())
print("Encrypted:", encrypted)

decrypted = fernet.decrypt(encrypted)
print("Decrypted:", decrypted.decode())
