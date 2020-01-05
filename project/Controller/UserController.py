
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



