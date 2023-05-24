import sqlite3


def insert(*, username: str, passwd: str, email: str):
    db = sqlite3.connect('users.db')
    c = db.cursor()

    c.execute(f"INSERT INTO 'users' (username, passwd, email) VALUES (?, ?, ?)", (username, passwd, email))

    db.commit()
    c.close()


def check(**parameters: str):
    db = sqlite3.connect('users.db')
    c = db.cursor()
    for parameter, invalue in parameters.items():
        user = c.execute(f"SELECT {parameter} FROM users")
        value = user.fetchall()
        if invalue == value[0][0]:
            return True
        elif invalue != value[0][0]:
            pass

    c.close()


def update(*, user: str, **parameters: str):
    db = sqlite3.connect('users.db')
    c = db.cursor()
    c.execute(f"SELECT * FROM users WHERE username = '{user}'")
    for parameter, value in parameters.items():
        try:
            c.execute(f"UPDATE users SET '{parameter}' = '{value}' WHERE username = '{user}'")
        except sqlite3.OperationalError:
            pass

    db.commit()
    c.close()


def delete(*, user: str):
    db = sqlite3.connect('users.db')
    c = db.cursor()
    c.execute(f"DELETE FROM users WHERE username = '{user}'")
    db.commit()
    c.close()
