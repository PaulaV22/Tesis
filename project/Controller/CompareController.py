
import numpy as np
from project.model.HaplotypesSearcher import HaplotypesSearcher
import os
import sys

class CompareController():

    def __init__(self):
        self.HS = HaplotypesSearcher()
        self.dbList = self.getDatabases()
        self.dbName = self.HS.getDatabases()[0]

    def resourcePath(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        output = base_path + relative_path
        return output

    def getDatabases(self):
        output = []
        dbs= self.resourcePath("/Databases")
        for dir in os.listdir(dbs):
            output.append(dir)
        output.sort()
        return output

    def getDb(self):
        self.dbList = self.getDatabases()
        selectedIndex = self.window.selectDatabase.currentIndex()
        dbName = self.dbList[selectedIndex]
        return dbName


    def setDb(self, dbName):
        self.dbName= dbName
        self.HS.setDb(dbName)

    def compare(self, sequence, numResults, database):
        if not self.HS:
            self.HS = HaplotypesSearcher()
        self.HS.setDb(database)
        seqName = sequence.partition('\n')[0]
        seqName = seqName[1:]
        seqName = seqName.replace("\r", "")
        seqName = seqName.replace("\n", "")

        seqPath = "/Temp/"+ seqName+ ".fa"

        tempFile = self.resourcePath(seqPath)
        print(tempFile)
        file = open(seqPath, "w+")

        file.write(sequence)
        file.close()
        print(numResults)
        results = self.HS.getResults(seqName,seqPath,database,numResults)
        return results

    def showResults(self, results):
        dt = np.dtype('string', 'float', 'int')
        resultsArray = np.array(results, dtype=dt)
        return resultsArray
        # self.drawTable(results)


