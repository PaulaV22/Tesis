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

        self.setDb(self.db, dbName)

        self.dbAdmin = DbAdmin.DbAdmin()
        #self.dbAdmin = DB.DbAdmin()

    def resourcePath(self,relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        output = base_path + relative_path
        output = output.replace("\\", "/")
        return output


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

