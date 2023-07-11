from django.apps import AppConfig
from flask import Flask, render_template, request, redirect
import mysql.connector
from config.DBconfig import DB_CONFIG

app = Flask(__name__)

# 데이터베이스 연결 설정
db = mysql.connector.connect(**DB_CONFIG)


class IndexConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'index'


@app.route('/')
def home():
    if 'username' in session:
        username = session['username']
        return f'Hello, {username}! You are logged in.'
    else:
        return 'You are not logged in.'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 데이터베이스에서 사용자 정보 확인
        cursor = db.cursor()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['username'] = user[1]
            return redirect('/')
        else:
            return 'Invalid username or password'
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)