from flask import Flask, render_template, request,url_for,redirect, g, flash, current_app, session, make_response
from config import host, user, password, db_name
import psycopg2
from dotenv import load_dotenv
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from user_login import UserLogin
from Fdatabase import Fdatabase
from werkzeug.security import generate_password_hash, check_password_hash


load_dotenv()

app = Flask(__name__)
login_manager = LoginManager(app)

app.config["SECRET_KEY"] = 'cb8b35c2a2a4d4f56c6408b7873b6789671a4948'

# operators = ['Ivanov Ivan', 'Soloviev Dmitrii', 'Avdeed Igor']
result_list = ['ЧИСТ.','НАРУШ.','НЕ ПРОП.']

@login_manager.user_loader
def load_user(user_id):
    # print(f'load_user {user_id}')
    return UserLogin().fromDB(user_id, dbase)

def connect_db():
    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database='test')
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
    # print('[INFO]: init db in before request')

@app.teardown_appcontext
def close_connection(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()
        # print('[INFO]: close connection in teardown')

@app.route('/')
def index():
    # print('[INFO]: in the index route')
    return render_template('index.html', title= "Sovkombank")



@app.route('/profile/<username>')
@login_required
def profile(username= None):
    return render_template('profile.html', username = username)

@app.route('/register', methods=["POST", "GET"])
def register():
    error = None
    if request.method == "POST":
        if len(request.form['username']) > 4 and len(request.form['password1']) > 4 \
            and request.form['password1'] == request.form["password2"]:
            hash = generate_password_hash(request.form["password1"])
            res = dbase.addUser(request.form['username'], hash)
            if res:
                flash('Вы успешно зарегистрированы')
                flash('Введите выши данные в форму авторизации и войдите')
                return redirect(url_for('login'))
            else:
                error = 'Пользователь с таким именем уже существует'
        else:
            error = 'Неверно заполнены поля, минимум 5 символов'

    return render_template('register.html', title= "Регистрация", error = error)


@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == "POST":
        user = dbase.getUserByUsername(request.form['username'].strip())
        if user and check_password_hash(user[2], request.form['password']):
            flash('Успешный вход, доступ открыт')
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            # session['userlogged'] = request.form['username']
            return redirect(url_for('profile', username = request.form['username']))
        else:
            error = 'Не верно введены данные форм, проверьте правильность имени и пароля'
        
    return render_template('login.html', title = 'Авторизация', error = error)

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



@app.route('/choose',methods=["POST", "GET"])
@login_required
def choose():
    operators = dbase.getOperators()
    # print(f"[INFO]: имя оператора {operators}")
    if request.method == "POST":
        response = make_response(redirect(url_for('showreq')))
        response.set_cookie('operator',request.form['operators'])
        return response
        
    return render_template('choose_operator.html', title= "Выберите оператора", operators = operators)


@app.route('/showreq', methods=["POST", "GET"])
@login_required
def showreq():
    op_name = request.cookies.get('operator') 
    # print(f"[INFO]: имя оператора {op_name}")
    op_id = dbase.getOpId(op_name)
    # print(f"[INFO]: operator_id =  {op_id}")
    req_links = dbase.getListRequests(op_id) # Получение списка заявок оператора
    print(f"[INFO]: req_links =  {req_links}")
    return render_template('list_of_requests.html', title= "Список заявок", operator = op_name, requests_list = req_links)



@app.route('/showreq/<id>', methods=["POST", "GET"])
@login_required
def show_all_req(id):
    table_data = dbase.getAllData(id)
    request_id = table_data[0]
    contract_id = table_data[1]
    create_date = table_data[2].strftime('%d-%m-%Y %H:%M')
    is_delayed = ''
    if table_data[3] is True:
        is_delayed = 'Просрочена'
    else:
        is_delayed = 'Не просрочена'
    data = make_list(request_id, contract_id, create_date, is_delayed)
    # print(request_id, contract_id, create_date, is_delayed)
    # print(f'[INFO]: table_data = {table_data}')
    # data = (1257, 547, '2022-07-25 23:02', True)

    return render_template('request.html',id = id, data = data)


def make_list(*args):
    list_data = []
    for i in range(len(args)):
        list_data.append(args[i])
    return list_data



if __name__ == '__main__':
    app.run(debug=True)