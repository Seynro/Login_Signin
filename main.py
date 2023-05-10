from flask import Flask, render_template, request, flash, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

database = sqlite3.connect('datalogin.db', check_same_thread=False)
cursor = database.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    login TEXT,
    password TEXT
)""")
database.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')
        inp_login = request.form.get('login')
        inp_password = request.form.get('password')

        if action == 'login':
            return login_func(inp_login, inp_password)
        elif action == 'signin':
            return signin_func(inp_login, inp_password)

    return render_template('index.html')

def login_func(inp_login, inp_password):
    cursor.execute(f"SELECT login FROM users WHERE login = '{inp_login}'")
    if cursor.fetchone() is None:
        flash('Такого пользователя не существует')
        return redirect('/')
    else:
        cursor.execute(f"SELECT password FROM users WHERE login = '{inp_login}'")
        if cursor.fetchone()[0] == inp_password:
            flash('Вход прошёл успешно')
            return redirect('/')
        else:
            flash('Пароль неверный, попробуйте ещё')
            return redirect('/')

def signin_func(inp_login, inp_password):
    cursor.execute(f"SELECT login FROM users WHERE login = '{inp_login}'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users VALUES (?, ?)", (inp_login, inp_password))
        database.commit()
        flash('Аккаунт успешно создан')
        return redirect('/')
    else:
        flash('Такой логин уже существует')
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
