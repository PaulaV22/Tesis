import os
from project.model import HaplotypesSearcher as HaplotypeSearcher
from project.model import DbAdmin as DbAdmin
import sys

class Controller():
    def __init__(self):
        #self.projectPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.HS = HaplotypeSearcher.HaplotypesSearcher()
        self.dbAdmin = DbAdmin.DbAdmin()

    def resourcePath(self,relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        output = base_path + relative_path
        return output

    def getProjectPath(self):
        return self.projectPath

    def getDatabases(self):
        output = []
        dbs= self.resourcePath("/Databases")
        for dir in os.listdir(dbs):
            output.append(dir)
        output.sort()
        return output
