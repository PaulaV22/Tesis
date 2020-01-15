
import numpy as np
from project.model.HaplotypesSearcher import HaplotypesSearcher
from project.model.UserManager import UserManager as UM
import os
import sys

class UserController():

    def __init__(self):
        self.userManager = UM()

    def addUser(self, name, email, password):
        self.userManager.addUser(name,email,password)

    def getUser(self,email,password):
        user= self.userManager.getUser(email)
        if not user is None:
            if user['password']==password:
                return user
        return None

    def getUserByEmail(self,email):
        return self.userManager.getUser(email)

    def saveUser(self,user):
        return self.userManager.saveUser(user)

    def addDbToUser(self,id,dbName):
        return self.userManager.addDbToUser(id,dbName)