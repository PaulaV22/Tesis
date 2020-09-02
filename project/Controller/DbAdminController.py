
import numpy as np
from project.model.HaplotypesSearcher import HaplotypesSearcher
import os
import sys
import json
from project.Controller.Controller import Controller
from project.model import DbAdmin as DbAdmin


class DbAdminController(Controller):

    def __init__(self):
        Controller.__init__(self)


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
                    size = str(size)+ "kb"
                    openedFile= open(filePath,'r')
                    content = openedFile.read()
                    openedFile.close()
                    fileList.append({'name':file, 'size':size, 'content':content})
                output.append({'Name':dirName, 'Files':len(fileList),'FileList':fileList})
        salidaJson = json.dumps(output)
        return salidaJson


    def createDb(self, userId, dbName):
        dbPath = userId + "/" + dbName
        self.dbAdmin.configureDb(dbPath, dbName)

    def createSimpleDb(self, userId, dbName):
        dbPath = userId + "/" + dbName
        self.dbAdmin.configureSimpleDb(dbPath, dbName)

    def deleteDatabase(self,id,name):
        dbPath = id+"/"+name
        print("va a borrar "+dbPath)
        result = self.dbAdmin.deleteDb(dbPath,True)
        return result

    def deleteSequence(self,userid, db, sequenceName):
        seqPath = self.resourcePath("/Databases/"+ userid + "/" + db+"/"+sequenceName)
        print(seqPath)
        dbPath = userid+"/"+db
        result = self.dbAdmin.deleteSeq(dbPath,db,seqPath)
        print(result)
        return result

    def restartDb(self,userid, dbName):
        userDb =userid + "/" + dbName
        print("VA A RESTARTDB")
        self.dbAdmin.restartDb(userDb, dbName)