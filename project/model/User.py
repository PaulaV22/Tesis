from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json

class User(UserMixin):

    def __init__(self, name, email, password):
        self.email = email
        self.name = name
        self.password = generate_password_hash(password)
        self.dbs = []
        #self.is_anonymous = False
        self.is_admin = False

    def get_id(self):
        return self.email


    def toJson(self):
        output = {
            "email": self.email,
            "name": self.name,
            "password": self.password,
            "dbs": self.dbs,
        }
        return json.dumps(output)


    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False


    def __repr__(self):
        return '<User {}>'.format(self.email)