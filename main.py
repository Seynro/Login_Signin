import sqlite3

database = sqlite3.connect('datalogin.db')

cursor = database.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    login TEXT,
    password TEXT
)""")

database.commit()

###########################

# Вход
def login_func():
    inp_login = input("Login: ")
    cursor.execute(f"SELECT login FROM users WHERE login = '{inp_login}'")
    if cursor.fetchone() is None:
        print('Такого пользователя не существует')
        if input('Зарегистрируйтесь или попробуйте ещё: 1 или 2') == '1':
            signin_func()
        else:
            login_func()
    else:
        inp_password = input("Password: ")
        cursor.execute(f"SELECT password FROM users WHERE login = '{inp_login}'")
        if cursor.fetchone()[0] == inp_password:
            print('Вход прошёл успешно')
        else:
            print('Пароль неверный, попробуйте ещё')
            login_func()



# Регистрация

def signin_func():

    inp_login = input("Login: ")
    inp_password = input("Password: ")
    cursor.execute(f"SELECT login FROM users WHERE login = '{inp_login}'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users VALUES (?, ?)", (inp_login, inp_password))
        database.commit()
    else:
        if input('Такой логин уже существует, войдите в этот аккаунт или создайте новый: 1 или 2: ') == '1':
            return login_func()
        else:
            signin_func()
            print('Аккаунт успешно создан')

############################

if input('Вход или регистрация? 1 или 2?') == '1':
    login_func()

else:
    signin_func()


