import datetime as dt
from dotenv import load_dotenv


from flask import Flask, render_template, request, url_for,redirect, g, flash, current_app, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash


from config import host, user, password, db_name
from Fdatabase import Fdatabase
from user_login import UserLogin

load_dotenv()

app = Flask(__name__)
login_manager = LoginManager(app)

app.config["SECRET_KEY"] = 'cb8b35c2a2a4d4f56c6408b7873b6789671a4948'

@login_manager.user_loader
def load_user(user_id):
    print(f'load_user {user_id}')
    return UserLogin().fromDB(user_id, dbase)

def connect_db():
    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name)
    conn.autocommit = True
    return conn

def create_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

dbase = None
@app.before_request
def before_request():
    global dbase
    db = create_db()
    dbase = Fdatabase(db)
    print('[INFO]: init db in before request')

@app.teardown_appcontext
def close_connection(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()
        print('[INFO]: close connection in teardown')

@app.route('/')
def index():
    print('[INFO]: in the index route')
    return render_template('index.html', title= "Sovkombank")


@app.route('/workflow')
@login_required
def workflow():
    return render_template('workflow.html', title= "Рабочий стол")

@app.route('/profile/<username>')
@login_required
def profile(username= None):
    return render_template('profile.html', username = username)

@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if len(request.form['username']) > 4 and len(request.form['password1']) > 4 \
            and request.form['password1'] == request.form["password2"]:
            hash = generate_password_hash(request.form["password1"])
            res = dbase.addUser(request.form['username'], hash)
            if res:
                flash('Вы успешно зарегистрированы')
                return redirect(url_for('login'))
            else:
                flash('Пользователь с таким именем уже существует')
        else:
            flash('Неверно заполнены поля')

    return render_template('register.html', title= "Регистрация")


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        user = dbase.getUserByUsername(request.form['username'].strip())
        if user and check_password_hash(user[2], request.form['password']):
            flash('Успешный вход, доступ открыт')
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            # session['userlogged'] = request.form['username']
            return redirect(url_for('profile', username = request.form['username']))
        else:
            flash('Не верно введены данные форм, проверьте правильность имени и пароля')
        
    return render_template('login.html', title = 'Авторизация')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title = 'Страница не найдена')


@app.errorhandler(401)
def login_error(error):
    return render_template('page401.html', title = 'Пользователь не авторизован')


if __name__ == '__main__':
    app.run(debug=True)