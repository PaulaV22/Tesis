
import numpy as np
from project.model.HaplotypesSearcher import HaplotypesSearcher
import os
import sys
import json
from project.Controller.Controller import Controller

class CompareController(Controller):

    def __init__(self):
        Controller.__init__(self)
        self.HS = HaplotypesSearcher()
        #self.dbList = self.getDatabases()
        self.dbs = self.HS.getDatabases()
        self.dbName = ""
        if len(self.dbs)>0:
            self.dbName = self.dbs[0]


    def setDb(self, dbName):
        self.dbName= dbName
        self.HS.setDb(dbName)

    def compare(self, sequence, numResults, database, userId, ambiguo):
        if not self.HS:
            self.HS = HaplotypesSearcher()
        dbPath =userId+"/"+database

        print("dbPath es "+ dbPath)
        self.HS.setDb(dbPath, database)
        seqName = sequence.partition('\n')[0]
        seqName = ''.join(e for e in seqName if e.isalnum())

        seqPath = "/Temporal/"+ seqName+ ".fa"

        tempFile = self.resourcePath(seqPath)
        print("TEMP FILE IN PATH "+tempFile)
        with open(tempFile, "w+") as file:
            file.write(sequence)
            file.close()
        results = self.HS.getResults(seqName,tempFile,dbPath,numResults, ambiguo)
        try:
            os.remove(tempFile)
        except Exception as e:
            print(e)
        return results
        #return []

    def showResults(self, results):
        dt = np.dtype('string', 'float', 'int')
        resultsArray = np.array(results, dtype=dt)
        return resultsArray
        # self.drawTable(results)

    def createDb(self,userId,dbName):
        if not self.HS:
            self.HS = HaplotypesSearcher()
        dbPath = userId+"/"+dbName
        self.HS.configureDb(dbPath,dbName)

