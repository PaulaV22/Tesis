
import numpy as np
from project.model.HaplotypesSearcher import HaplotypesSearcher
import os
import sys
import json

class CompareController():

    def __init__(self):
        self.HS = HaplotypesSearcher()
        #self.dbList = self.getDatabases()
        self.dbs = self.HS.getDatabases()
        self.dbName = ""
        if len(self.dbs)>0:
            self.dbName = self.dbs[0]

    def resourcePath(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        output = base_path + relative_path
        return output

    def getDatabases(self, id):
        output = []
        dbs= self.resourcePath("/Databases/"+id)
        if not os.path.exists(dbs):
            os.mkdir(dbs)
        if len(os.listdir(dbs)) == 0:
            salidaJson = json.dumps(output)
            print(salidaJson)
            return salidaJson
        for base, dirs, files in os.walk(dbs):
            dirName = os.path.basename(os.path.normpath(base))
            if dirName!=id:
                fileList = []
                for file in files:
                    filePath = base + "/"+file
                    size = os.path.getsize(filePath)
                    size = size/1000
                    if size<0:
                        size = 1
                   # print(size)

                    size = str(size)+ "kb"
                    openedFile= open(filePath,'r')
                    content = openedFile.read()
                    openedFile.close()
                    fileList.append({'name':file, 'size':size, 'content':content})
                output.append({'Name':dirName, 'Files':len(fileList),'FileList':fileList})
        #for dir in os.listdir(dbs):
            #filesList = os.listdir(dir)
        salidaJson = json.dumps(output)
        print(salidaJson)
        return salidaJson

    def getDb(self):
        self.dbList = self.getDatabases()
        selectedIndex = self.window.selectDatabase.currentIndex()
        dbName = self.dbList[selectedIndex]
        return dbName


    def setDb(self, dbName):
        self.dbName= dbName
        self.HS.setDb(dbName)

    def compare(self, sequence, numResults, database, userId, ambiguo):
        if not self.HS:
            self.HS = HaplotypesSearcher()
        dbPath =userId+"/"+database
        print("userId es "+ userId)

        print("dbPath es "+ dbPath)
        self.HS.setDb(dbPath, database)
        seqName = sequence.partition('\n')[0]
        seqName = ''.join(e for e in seqName if e.isalnum())

        seqPath = "/Temp/"+ seqName+ ".fa"

        tempFile = self.resourcePath(seqPath)
        print(tempFile)
        file = open(seqPath, "w+")

        file.write(sequence)
        file.close()
        print(numResults)
        results = self.HS.getResults(seqName,seqPath,dbPath,numResults, ambiguo)
        return results
       # return []

    def compareWithSimpleDb(self,sequence, numResults, database, userId):
        if not self.HS:
            self.HS = HaplotypesSearcher()
        dbPath = userId + "/" + database

        self.HS.setDb(dbPath, database)
        seqName = sequence.partition('\n')[0]
        seqName = ''.join(e for e in seqName if e.isalnum())

        seqPath = "/Temp/" + seqName + ".fa"

        file = open(seqPath, "w+")

        file.write(sequence)
        file.close()
        print(numResults)
        results = self.HS.getResults(seqName, seqPath, dbPath, numResults,False)
        return results

    # return []
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

    def createDb(self, userId, dbName):
        if not self.HS:
            self.HS = HaplotypesSearcher()
        dbPath = userId + "/" + dbName
        self.HS.configureDb(dbPath, dbName)

    def createSimpleDb(self, userId, dbName):
        if not self.HS:
            self.HS = HaplotypesSearcher()
        dbPath = userId + "/" + dbName
        self.HS.configureSimpleDb(dbPath, dbName)



    def deleteDatabase(self,id,name):
        dbPath = id+"/"+name
        print("va a borrar "+dbPath)
        HS = HaplotypesSearcher()
        result = HS.deleteDb(dbPath,True)
        print (result)
        return result


    def deleteSequence(self,userid, db, sequenceName):
        HS = HaplotypesSearcher()
        seqPath = self.resourcePath("/Databases/"+ userid + "/" + db+"/"+sequenceName)
        print(seqPath)
        dbPath = userid+"/"+db
        result = HS.deleteSeq(dbPath,db,seqPath)
        print(result)
        return result

    def restartDb(self,userid, dbName):
        HS = HaplotypesSearcher()
        userDb =userid + "/" + dbName
        print("VA A RESTARTDB")
        HS.restartDb(userDb, dbName)