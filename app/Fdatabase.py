import psycopg2
from flask import url_for
from werkzeug.security import check_password_hash
import pytz
import datetime as dt

timedelta = dt.timedelta(hours=1)
timezone = pytz.timezone('Europe/Moscow')
now = dt.datetime.now(tz= timezone) - timedelta



class Fdatabase():
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def addUser(self, uname, passwd):
        try:
            self.__cur.execute(f"select count(*) from users where username like '{uname}'")
            res = self.__cur.fetchone()
            if res[0] > 0:
                print("Пользователь с таким именем уже существует")
                return False
            else:
                self.__cur.execute(f"insert into users(username, password) values ('{uname}','{passwd}')")
            

        except Exception as ex:
            print("Ошибка при запросе addUser",ex)
            return False

        return True

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = '{user_id} 'LIMIT 1;")
            res = self.__cur.fetchone()
            print(f'[INFO]: Ответ от базы данных при вызове метода getUser: {res}')
            if not res:
                print(f"[INFO]: Ответ от базы данных: {res}")
                return False
            return res
        except Exception as ex:
            print("[INFO] Ошибка при выборе из базы данных метода getUser")

        return False


    def getUserByUsername(self, username):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE username = '{username}'")
            res = self.__cur.fetchone()
            if not res:
                print(f'[INFO] результат ответа базы данных метод getUserByUsername: {res} ')
            else:
                print(f'[INFO] Данные метода getUserByUsername были получены: {res} ')
                return res
        except Exception as ex:
            print("[INFO] Ошибка при выборе из базы данных метода getUserByUsername")
            return False
        return False


    def getOperators(self):
        try:
            self.__cur.execute(f"SELECT DISTINCT op_name FROM operators;")
            res = self.__cur.fetchall()
            if not res:
                print(f'[INFO] результат ответа базы данных метод getOperators: {res} ')
            else:
                print(f'[INFO] Данные метода getOperators были получены: {res} ')
                list_of_operators = []
                for item in res:
                    list_of_operators.append(item[0])
                return list_of_operators
        except Exception as ex:
            print("[INFO] Ошибка при выборе из базы данных метода getOperators")
            return False
        return False


    def getListRequests(self, op_id):
        try:
            self.__cur.execute(f"SELECT id, request_id FROM requests WHERE operator_id = '{op_id}';")
            db_result = self.__cur.fetchall() 
            if not db_result:
                print(f'[INFO] результат ответа базы данных метод getListRequests: {db_result} ')
            else:
                print(f'[INFO] Данные метода getListRequest были получены: {db_result} ')
                req_links = []
                for item in db_result:
                    data = {'id': item[0], 'data': item[1]}
                    req_links.append(data)
                return req_links
        except Exception as ex:
            print("[INFO] Ошибка при выборе из базы данных метода getListRequests")
            return False
        return False
    

    def getAllDataInRequests(self, data):
        try:
            self.__cur.execute(f"SELECT o.id, o.name FROM operators o WHERE requests = '{data}';")
            result = self.__cur.fetchone() 
            if not result:
                print(f'[INFO] результат ответа базы данных метод getAllDataInRequests: {result} ')
            else:
                print(f'[INFO] Данные метода getAllDataInRequests были получены: {result} ')
                return result
        except Exception as ex:
            print("[INFO] Ошибка при выборе из базы данных метода getAlldataInRequests")
            return False
        return False

    def getOpId(self, op_name):
        try:
            self.__cur.execute(f"SELECT id FROM operators WHERE op_name = '{op_name}';")
            db_result = self.__cur.fetchone() 
            if not db_result:
                print(f'[INFO] результат ответа базы данных метод getOpID: {db_result[0]} ')
            else:
                print(f'[INFO] Данные метода getOpId были получены: {db_result[0]} ')
                return db_result[0]
        except Exception as ex:
            print("[INFO] Ошибка при выборе из базы данных метода getOpId")
            return False
        return False

    def getAllData(self, id):
        try:
            self.__cur.execute(f"SELECT request_id, contract_id, created, is_delayed FROM requests WHERE id = '{id}';")
            db_result = self.__cur.fetchone() 
            if not db_result:
                print(f'[INFO] результат ответа базы данных метод getOAllData: {db_result} ')
            else:
                print(f'[INFO] Данные метода getAllData были получены: {db_result} ')
                return db_result
        except Exception as ex:
            print("[INFO] Ошибка при выборе из базы данных метода getOpId")
            return False
        return False