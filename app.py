from flask import Flask,render_template,request,redirect
import psycopg2

app = Flask(__name__)
connection = psycopg2.connect(database='mywebapp',
                                user='postgres',
                                password='qwerty',
                                host='127.0.0.1')
connection.autocommit = True

cursor = connection.cursor()
ex = list()
@app.route('/login', methods=['post', 'get'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            attention = 'Ошибка! Поля пустые.'

            if username == '' or password == '':
                return render_template('login.html', attention = attention)
            else:
                try:
                    cursor.execute('SELECT * FROM service.users WHERE login=%s AND password=%s',
                                    (str(username), str(password)))
                    records = cursor.fetchall()
                    if len(records) != 0:
                        return render_template('account.html',full_name = records[0][1],login = username,password=password)
                    else:
                        return render_template('login.html', attention=attention)
                except Exception as _ex:
                    print(_ex)
                finally:
                    if connection:
                        connection.close()
                        print('Closed')
        elif request.form.get("registration"):
            return redirect("/registration")
    return render_template('login.html')


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('username')
        password = request.form.get('password')
        attention = "Поля пустые!"
        attention2 = 'Пользователь с таким логином уже существует!'
        if name == '' or login == '' or password == '':
            return render_template('registration.html', attention=attention)
        else:
            cursor.execute(f"""SELECT * FROM service.users WHERE login='{login}'""")
            result = cursor.fetchall()
            if len(result) != 0:
                return render_template('registration.html', attention2=attention2)
            else:
                cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                            (str(name), str(login), str(password)))
                return redirect('/login')
    return render_template('registration.html')




if __name__ == '__main__':
    app.run(debug=True)
