import sys
import os
import json
from project.model.User import User

class UserManager():

    def __init__(self):
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
            print(jsonUser)
            if (jsonUser['email'] == email):
                raise Exception('The user already exists')
        newUser = User(name,email,password)
        self.users.append(newUser.toJson())
        with open("users.json", mode='w', encoding='utf-8') as f:
            json.dump(self.users, f)

    def deleteUser(self, email):
        i = 0
        while i < len(self.users) and self.users[i].email!=email:
            i += 1
        if (i<len(self.users)):
            del self.users[i]
        with open("users.json", mode='w', encoding='utf-8') as f:
            json.dump(self.users, f)

    def setDbs(self, dbs):
        self.dbs = dbs
        self.saveToDb()

    def getUser(self, email):
        for user in self.users:
            print(user)
            jsonUser = json.loads(user)
            if jsonUser['email'] == email:
                return jsonUser
        return None

    def getUserDbs(self,email):
        user = self.getUser(email)
        if user is None:
            return []
        return user.dbs

    def saveUser(self,user):
        for i in range(len(self.users)):
            u = self.users[i]
            jsonUser = json.loads(u)
            print(jsonUser)
            if (jsonUser['email'] == user['email']):
                jsonUser['name'] = user['name']
                jsonUser['password'] = user['password']
                jsonUser['logged'] = user['logged']
            self.users[i] = json.dumps(jsonUser)
        with open("users.json", mode='w', encoding='utf-8') as f:
            json.dump(self.users, f)

    def addDbToUser(self,email,db):
        user = self.getUser(email)
        userDbs = user['dbs']
        if db in userDbs:
            print("ya existe la db")
            return None
        else:
            userDbs.append(db)
            print(userDbs)
            user['dbs'] = userDbs
            print(user)
            self.saveUser(user)
            return user
