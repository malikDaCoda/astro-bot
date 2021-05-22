import bcrypt
from helpers.encryption import Encryption

# hash and salt password
def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

# checks if password is valid
def valid_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

# wrapper to encrypt data with password
def encrypt(data, password):
    e = Encryption(password.encode())
    return e.encrypt(data.encode()).decode()

# wrapper to decrypt data with password
def decrypt(data, password):
    e = Encryption(password.encode())
    return e.decrypt(data.encode()).decode()


# get master password of user
def get_password(users, uid):
    if users.get(uid):
        return users[uid].get("masterpass")
    return None
