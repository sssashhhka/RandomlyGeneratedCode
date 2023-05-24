import hashlib


def hash_pass(password: str):
    hash_password = hashlib.sha3_256()
    password = password.encode()
    hash_password.update(password)
    hash_password = hash_password.hexdigest()
    return hash_password
