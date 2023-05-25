import sqlite3


def insert(*, username: str, passwd: str, email: str, theme: str = 'dark'):  # Insert values in database
    db = sqlite3.connect('users.db')
    c = db.cursor()

    c.execute(f"UPDATE users SET 'isCurrent' = '0' WHERE isCurrent = '1'")
    c.execute(f"INSERT INTO 'users' (username, passwd, email, theme, isCurrent) VALUES (?, ?, ?, ?, ?)", (username,
                                                                                                          passwd, email,
                                                                                                          theme, 1))

    db.commit()
    c.close()


def check(**parameters: str):  # Returns True if parameter's value exist
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


def get(username: str, *args: str):  # Returns list parameters
    db = sqlite3.connect('users.db')
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


def update(*, user: str, **parameters: str):  # Updates values in database
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


def delete(*, user: str):  # Delete values from database
    db = sqlite3.connect('users.db')
    c = db.cursor()
    c.execute(f"DELETE FROM users WHERE username = '{user}'")
    db.commit()
    c.close()
