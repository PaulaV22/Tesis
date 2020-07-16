import project.model.SimpleDbCreator as SC
import project.model.SimpleBlast as S
from project.model import AmbiguousDbCreator as AC, GlobalBlast as GC
from project.model import DbAdmin as DbAdmin
import project.model.ResultsAnalizer as RA
import os
import shutil
import json
import sys

class HaplotypesSearcher():

    def __init__(self, dbName=None):
        if (dbName):
            self.db=dbName
        else:
            self.db = "BoLa"
        self.projectPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.categories  = {"ALTA": 1, "MEDIA": 1, "BAJA": 1}
        self.categoriesPath = self.projectPath+"/Categories"
        self.setDb(self.db, dbName)
        if not os.path.exists(self.categoriesPath):
            os.makedirs(self.categoriesPath)
        self.option="compare"
        self.newDb=None
        self.dbAdmin = DbAdmin.DbAdmin()
        #self.dbAdmin = DB.DbAdmin()

    def resourcePath(self,relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        output = base_path + relative_path
        output = output.replace("\\", "/")
        return output

    def setOption(self,option):
        self.option=option

    def setNewDb(self,newDb):
        self.newDb=newDb

    def getResults(self,queryName,queryPath, database, numSeqs, ambiguo):
        print("GET RESULTS")
        db = ""
        if ambiguo:
            db ="DbAmbigua"
        else:
            db ="Blastdb"
        simpleBlast = S.SimpleBlast(db, "salida", "salida", "fasta", "FinalResult", database, True)
        simpleBlast.align(queryPath, queryName)

        resultsAnalizer = RA.ResultsAnalizer("FinalResult",database, ambiguo)

        results = resultsAnalizer.getSimilarSequences(queryName,numSeqs)
        self.dbAdmin.deleteDb(database, False, False)
        return results

    def setAddSeqValues(self, path, content,name):
        self.path = path
        self.newSeqContent = content
        self.newSeqName = name

    def setSequenceToDelete(self, seqPath):
        self.sequenceToDelete = seqPath

    def setQueryData(self,queryName, numSeqs):
        self.queryName = queryName
        self.numSeqs = numSeqs

    def probarGlobalComparator(self):
        self.globalBlast.align("BoLa")

    def probarAmbiguousDbCreator(self):
        self.ambiguousDbCreator.makeDb()
        query = self.resourcePath('/BoLa/prueba.fa')
        self.simpleBlast.align(query, "prueba")

    def probarSimpleDbCreator(self):
        self.simpleDbCreator.makeDb()


    def deleteseqAdmin (self, db, sequence):
        self.dbAdmin.deleteSequence(self.projectPath,db,sequence)


    def configureDb2(self, db):
        ####crear la bd con los archivos originales de BoLa####
        ready = False
        self.simpleDbCreator.makeDb()
        ####alinear todas las secuencias de BoLa entre si generando un archivo de salida por cada alineacion (n x n)####
        while not ready:
            try:
                self.globalBlast.align("/Databases/"+db)
                ready = True
            except:
                self.simpleDbCreator.makeDb()
                ready = False
        ####armar la base de datos con las posibles combinaciones (Nuevadb)####
        self.ambiguousDbCreator.makeDb()
        categories = {}
        #categoriesFile = self.projectPath + "/Categories/" + db + ".json"
        categoriesFile = self.resourcePath("/Categories/" + db + ".json")

        with open(categoriesFile, mode='w+') as f:
            json.dump(categories, f)

    def getDatabases(self):
        output = []
        dbs= self.resourcePath("\Databases")
        print(dbs)
        for dir in os.listdir(dbs):
            output.append(dir)
        output.sort()
        return output

    def getDb(self):
        return self.resourcePath('\Databases\\'+self.db)

    def getDbName(self):
        return self.db

    def setDb(self, dbPath, dbName):
        self.db = dbPath
        self.simpleDbCreator = SC.SimpleDbCreator("Databases/" + dbPath, "Blastdb",
                                                  dbName, "secuencias", "fasta")
        self.globalBlast = GC.GlobalBlast("Blastdb", "secuencias", "salida", "fasta", "BlastResult", dbPath)
        self.ambiguousDbCreator = AC.AmbiguousDbCreator("BlastResult", "Nuevadb" , "salida", "fasta", "DbAmbigua", dbPath)
        self.simpleBlast = S.SimpleBlast("DbAmbigua", "salida", "salida", "fasta", "FinalResult", dbPath, True)
        self.resultsAnalizer = RA.ResultsAnalizer("FinalResult",dbPath,True)


    def getProjectPath(self):
        return self.projectPath

searcher = HaplotypesSearcher()
searcher.getDatabases()
