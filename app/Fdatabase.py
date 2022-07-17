import psycopg2
from flask import url_for
from werkzeug.security import check_password_hash



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
            print("[INFO] Ошибка при выборе из базы данных")

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
            # hash = str(res[1])
            # print(f'[INFO] ответ от БД при уточнении наличия пользователя в БД: {res[1]}')
            # if not res:
            #     print(f'[INFO] Пользователя нет в базе данных')
            #     return False
            # else:
            #     if check_password_hash(hash, password):
            #         print('[INFO] Пароли совпадают')
            #         return True
                    
            #     print('[INFO] Не верно введен пароль')
        except Exception as ex:
            print("[INFO] Ошибка при выборе из базы данных")
            return False
        return False
           