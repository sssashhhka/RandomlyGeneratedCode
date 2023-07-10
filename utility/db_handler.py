import sqlite3
import time
import os

version: str = f"OS: [{os.name}] db_handler v.1.0_rc (release candidate)"


def log_print(info: str, state: int = 0):
    if os.path.isfile("logs/log.txt"):
        f = open("logs/log.txt", "a+")
    else:
        f = open("logs/log.txt", "w+")
    time_is = time.strftime("%X")
    info_state = None
    match state:
        case 0:
            info_state = "Info"
        case 1:
            info_state = "Warning"
        case 2:
            info_state = "Error"
    print(f"[{time_is}][{info_state}] {info}")
    f.write(f"[{time_is}][{info_state}] {info}\n")
    f.close()


def init():
    print(version)
    try:
        db = sqlite3.connect("users/users.db")
        c = db.cursor()
        c.execute("SELECT * FROM USERS")
    except sqlite3.OperationalError:
        db = sqlite3.connect("users/users.db")
        c = db.cursor()
        c.execute("""CREATE TABLE users (
            username TEXT,
            passwd TEXT,
            email TEXT,
            theme TEXT,
            isCurrent TEXT,
            clrtheme TEXT
        )""")
        db.commit()
        c.close()
    else:
        log_print("Database initialized.")


def insert(*, username: str, passwd: str, email: str, theme: str = 'Dark', clrtheme: str = 'dark-blue'):
    db = sqlite3.connect('users/users.db')
    c = db.cursor()

    c.execute(f"UPDATE users SET 'isCurrent' = '0' WHERE isCurrent = '1'")
    c.execute(f"INSERT INTO 'users' (username, passwd, email, theme, isCurrent, clrtheme) VALUES (?, ?, ?, ?, ?, ?)",
              (username, passwd, email, theme, 1, clrtheme))

    db.commit()
    c.close()
    log_print("Userdata successfully wrote.")


def check(*, return_param: str, **parameters: str):
    db = sqlite3.connect('users/users.db')
    c = db.cursor()
    if return_param == 'Boolean':
        for parameter, invalue in parameters.items():
            user = c.execute(f"SELECT * FROM users WHERE {parameter} = '{invalue}'")
            value = user.fetchone()
            try:
                if invalue in value:
                    return True
                else:
                    pass
            except TypeError:
                return False
    elif return_param != 'Boolean':
        try:
            for parameter, invalue in parameters.items():
                user = c.execute(f"SELECT {return_param} FROM users WHERE {parameter} = '{invalue}'")
                value = user.fetchall()
                return value[0][0]
        except IndexError:
            return None

    c.close()


def get(username: str, *args: str) -> list:
    db = sqlite3.connect("users/users.db")
    c = db.cursor()
    parameters_list = []
    for parameter in args:
        try:
            user = c.execute(f"SELECT {parameter} FROM users WHERE username = '{username}'")
            value = user.fetchone()
            try:
                parameters_list.append(value[0])
            except TypeError:
                log_print(f'Bad username [{username}].', 1)
        except sqlite3.OperationalError:
            log_print(f'Bad parameter name [{parameter}].', 2)
    c.close()
    return parameters_list


def update(*, user: str, **parameters: str):
    db = sqlite3.connect('users/users.db')
    c = db.cursor()
    c.execute(f"SELECT * FROM users WHERE username = '{user}'")
    for parameter, value in parameters.items():
        try:
            c.execute(f"UPDATE users SET '{parameter}' = '{value}' WHERE username = '{user}'")
            log_print("Userdata successfully updated.")
        except sqlite3.OperationalError:
            log_print(f"Bad parameters [{parameters.items()}].", 2)

    db.commit()
    c.close()


def delete(*, user: str):
    db = sqlite3.connect('users/users.db')
    c = db.cursor()
    c.execute(f"DELETE FROM users WHERE username = '{user}'")
    db.commit()
    c.close()
    log_print(f"User {user} deleted.")


if __name__ != "__main__":
    init()
