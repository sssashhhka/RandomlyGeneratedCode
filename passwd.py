import hashlib


def passwd(password: str):
    hash_pass = hashlib.sha3_256()
    password = password.encode()
    hash_pass.update(password)
    hash_pass = hash_pass.hexdigest()
    return hash_pass
