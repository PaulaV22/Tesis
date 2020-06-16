from project.Manager.UserManager import UserManager as UM
from flask_login import LoginManager

class UserController():

    def __init__(self):
        self.userManager = UM()

    def addUser(self, name, email, password):
        self.userManager.addUser(name,email,password)

    def getUser(self,email):
        return  self.userManager.getUser(email)


    def getUserByEmail(self,email):
        return self.userManager.getUser(email)

    def saveUser(self,user):
        return self.userManager.saveUser(user)

    def addDbToUser(self,id,dbName):
        return self.userManager.addDbToUser(id,dbName)