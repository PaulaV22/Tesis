import os
import sys
import shutil
from shutil import copyfile
import subprocess
import project.model.SimpleBlast as SB
import project.model.SimpleDbCreator as SC
import project.model.SimpleBlast as S
from project.model import AmbiguousDbCreator as AC, GlobalBlast as GC

class DbAdmin:

    def __init__(self, dbName=None):
        if (dbName):
            self.database=dbName
        else:
            self.database = "BoLa"
        self.projectPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.categories  = {"ALTA": 1, "MEDIA": 1, "BAJA": 1}
        self.categoriesPath = self.projectPath+"/Categories"
        self.setDb(self.database, dbName)
        if not os.path.exists(self.categoriesPath):
            os.makedirs(self.categoriesPath)
        self.newDb=None
        #self.databaseAdmin = DB.DbAdmin()

    def resourcePath(self,relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        output = base_path + relative_path
        output = output.replace("\\", "/")
        return output

    def setDb(self, dbPath, dbName):
        self.database = dbPath
        self.simpleDbCreator = SC.SimpleDbCreator("Databases/" + dbPath, "Blastdb",
                                                  dbName, "secuencias", "fasta", True)
        self.globalBlast = GC.GlobalBlast("Blastdb", "secuencias", "salida", "fasta", "BlastResult", dbPath)
        self.ambiguousDbCreator = AC.AmbiguousDbCreator("BlastResult", "Nuevadb" , "salida", "fasta", "DbAmbigua", dbPath)
        self.simpleBlast = S.SimpleBlast("DbAmbigua", "salida", "salida", "fasta", "FinalResult", dbPath, True)

    def configureDb(self, dbPath, dbName):
        ####crear la bd con los archivos originales de BoLa####
        ready = False
        simpleDbCreator = SC.SimpleDbCreator("Databases/" + dbPath, "Blastdb", dbName, "secuencias", "fasta", True)

        globalBlast = GC.GlobalBlast("Blastdb", "secuencias", "salida", "fasta", "BlastResult", dbPath)
        ambiguousDbCreator = AC.AmbiguousDbCreator("BlastResult", "Nuevadb", "salida", "fasta", "DbAmbigua",dbPath)
        #simpleBlast = S.SimpleBlast("DbAmbigua", "salida", "salida", "fasta", "FinalResult", dbPath, True)
        #self.resultsAnalizer = RA.ResultsAnalizer("FinalResult", self.database, self.categories, self.categoriesPath)
        print("llama a simple db creator make db")
        simpleDbCreator.makeDb()
        ####alinear todas las secuencias de BoLa entre si generando un archivo de salida por cada alineacion (n x n)####
        while not ready:
            try:
                print("global blast va a alinear "+dbPath)
                globalBlast.align("Databases/"+dbPath)
                ready = True
            except:
                print(" hubo error y sismpledbcreator va a crear db de nuevo ")
                simpleDbCreator.makeDb()
                ready = False
        ####armar la base de datos con las posibles combinaciones (Nuevadb)####
        print(" ambiguousdbcreator va a makeDb ")

        ambiguousDbCreator.makeDb()
        self.deleteDb(dbPath, False, False)
        #categoriesFile = self.projectPath + "/Categories/" + db + ".json"

    def configureSimpleDb(self, dbPath, dbName):
        print("To create simple db")
        simpleDbCreator = SC.SimpleDbCreator("Databases/" + dbPath, "Blastdb", dbName, "secuencias", "fasta", False)
        simpleDbCreator.makeDb()
        print("Simple db created "+dbName)


    def deleteDb(self,db,ambigua=True, total=True):
        Database = self.resourcePath('/Databases/' + db)
        Blastdb = self.resourcePath('/Blastdb/' + db)
        BlastResult = self.resourcePath('/BlastResult/' + db)
        DbAmbigua = self.resourcePath('/DbAmbigua/' + db)
        FinalResult = self.resourcePath('/FinalResult/' + db)
        if total:
            try:
                shutil.rmtree(Database)
            except:
                print("error deleting from Database")
                pass
        try:
            shutil.rmtree(Blastdb)
        except:
            print("error deleting from Blastdb")
            pass
        try:
            shutil.rmtree(BlastResult)
        except:
            print("error deleting from BlastResult")
            pass
        if ambigua:
            try:
                shutil.rmtree(DbAmbigua)
            except:
                print("error deleting from DbAmbigua")
                pass
        try:
            shutil.rmtree(FinalResult)
        except:
            print("error deleting from FinalResult")
            return "Error in a deletion"
        print("borro todo")
        return "Deleted ok"

    def deleteSeq(self, userDb, dbName, seqPath):
        try:
            os.remove(seqPath)
            self.restartDb(userDb, dbName)
        except:
            print("La carpeta no existe")
        self.configureDb(userDb,dbName)
        return "removed ok"


    def addSeq(self, path,db, name, seq):
        file = open(path+"/"+name+".fa", "w")
        file.write(">"+name + os.linesep)
        file.write(seq)
        file.close()
        self.restartDb(db)


    def restartDb(self,userDb, dbName):
        self.deleteDb(userDb, True, False)
        print("termino de borrar. Va a configureDb con "+ userDb +" "+dbName)
        self.configureDb(userDb, dbName)