import sqlite3


def init():
    try:
        db = sqlite3.connect("../databases/users.db")
        c = db.cursor()
        c.execute("SELECT * FROM USERS")
    except sqlite3.OperationalError:
        db = sqlite3.connect("../databases/users.db")
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


def insert(*, username: str, passwd: str, email: str, theme: str = 'Dark', clrtheme: str = 'dark-blue'):
    db = sqlite3.connect('../databases/users.db')
    c = db.cursor()

    c.execute(f"UPDATE users SET 'isCurrent' = '0' WHERE isCurrent = '1'")
    c.execute(f"INSERT INTO 'users' (username, passwd, email, theme, isCurrent, clrtheme) VALUES (?, ?, ?, ?, ?, ?)",
              (username, passwd, email, theme, 1, clrtheme))

    db.commit()
    c.close()


def check(*, return_param: str, **parameters: str):
    db = sqlite3.connect('../databases/users.db')
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


def get(username: str, *args: str):
    db = sqlite3.connect("../databases/users.db")
    c = db.cursor()
    parameters_list = []
    for parameter in args:
        try:
            user = c.execute(f"SELECT {parameter} FROM users WHERE username = '{username}'")
            value = user.fetchone()
            try:
                parameters_list.append(value[0])
            except TypeError:
                print(f'Bad username [{username}]')
        except sqlite3.OperationalError:
            print(f'Bad parameter name [{parameter}]')
    c.close()
    return parameters_list


def update(*, user: str, **parameters: str):
    db = sqlite3.connect('../databases/users.db')
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
    db = sqlite3.connect('../databases/users.db')
    c = db.cursor()
    c.execute(f"DELETE FROM users WHERE username = '{user}'")
    db.commit()
    c.close()


if __name__ != "__main__":
    init()
