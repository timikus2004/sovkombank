from flask_login import current_user


class UserLogin():
    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user[0])

    def get_name(self):
        return self.__user[1] if self.__user else "Без имени"

    
