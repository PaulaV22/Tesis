from flask_login import LoginManager
from project.Controller.Controller import Controller
import json, sys, os
from project.model.User import User

class UserController(Controller):

    def __init__(self):
        Controller.__init__(self)
        usersPath = self.resourcePath('/users.json')
        with open(usersPath, 'r') as f:
            self.users = json.load(f)
        print(self.users)

    def resourcePath(self,relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        output = base_path + relative_path
        return output


    def addUser(self, name, email, password):
        for user in self.users:
            print(user)
            jsonUser = json.loads(user)
            if (jsonUser['email'] == email):
                raise Exception('The user already exists')
        newUser = User(name,email,password)
        newUser.password = newUser.set_password(password)
        print(newUser)
        self.users.append(newUser.toJson())
        with open("users.json", mode='w', encoding='utf-8') as f:
            json.dump(self.users, f)


    def getUser(self,email):
        for user in self.users:
            print(user)
            jsonUser = json.loads(user)
            if jsonUser['email'] == email:
                return User(jsonUser['name'], jsonUser['email'], jsonUser['password'])
        return None


    def saveUser(self,user):
        for i in range(len(self.users)):
            u = self.users[i]
            jsonUser = json.loads(u)
            print(jsonUser)
            if (jsonUser['email'] == user.email):
                jsonUser['name'] = user.name
                jsonUser['password'] = user.password
                self.users[i] = json.dumps(jsonUser)
        with open("users.json", mode='w', encoding='utf-8') as f:
            json.dump(self.users, f)
