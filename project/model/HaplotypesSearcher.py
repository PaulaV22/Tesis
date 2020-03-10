import project.model.SimpleDbCreator as SC
import project.model.SimpleBlast as S
from project.model import AmbiguousDbCreator as AC, GlobalBlast as GC
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
        #self.dbAdmin = DB.DbAdmin()

    def resourcePath(self,relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        output = base_path + relative_path
        return output

    def setOption(self,option):
        self.option=option

    def setNewDb(self,newDb):
        self.newDb=newDb

    def getResults(self,queryName,queryPath, database, numSeqs, ambiguo):
        db = ""
        if ambiguo:
            db ="DbAmbigua"
        else:
            db ="BlastDb"
        simpleBlast = S.SimpleBlast(db, "salida", "salida", "fasta", "FinalResult", database, True)
        simpleBlast.align(queryPath, queryName)

        resultsAnalizer = RA.ResultsAnalizer("FinalResult",database, ambiguo)

        results = resultsAnalizer.getSimilarSequences(queryName,numSeqs)

        return results



    def run(self):
    #def searchHaplotypes(self):
        if self.option=="compare":
            #queryPath = self.projectPath + "/" +self.queryName
            queryPath = self.resourcePath("/"+self.queryName)
            # alinear y obtener resultados de la query deseada
            self.simpleBlast.align(queryPath, self.queryName)
            results = self.resultsAnalizer.getSimilarSequences(self.numSeqs)
            return results
            #return results
        if self.option=="configuredb":
            self.configureDb(self.newDb)

        if self.option=="deletedb":
            self.deleteDb(self.db)
        if self.option=="deleteSeq":
            self.deleteSeq(self.db, self.sequenceToDelete)
        if self.option=="addSeq":
            self.addSeq(self.path,self.db,self.newSeqName, self.newSeqContent)

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

    def configureDb(self, dbPath, dbName):
        ####crear la bd con los archivos originales de BoLa####
        ready = False
        simpleDbCreator = SC.SimpleDbCreator("Databases/" + dbPath, "Blastdb", dbName, "secuencias", "fasta")

        globalBlast = GC.GlobalBlast("Blastdb", "secuencias", "salida", "fasta", "BlastResult", dbPath)
        ambiguousDbCreator = AC.AmbiguousDbCreator("BlastResult", "Nuevadb", "salida", "fasta", "DbAmbigua",dbPath)
        #simpleBlast = S.SimpleBlast("DbAmbigua", "salida", "salida", "fasta", "FinalResult", dbPath, True)
        #self.resultsAnalizer = RA.ResultsAnalizer("FinalResult", self.db, self.categories, self.categoriesPath)
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
        #categoriesFile = self.projectPath + "/Categories/" + db + ".json"

    def configureSimpleDb(self, dbPath, dbName):
        simpleDbCreator = SC.SimpleDbCreator("Databases/" + dbPath, "Blastdb", dbName, "secuencias", "fasta")
        simpleDbCreator.makeDb()


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

    def restartDb(self,userDb, dbName):
        self.deleteDb(userDb, False)
        print("termino de borrar. Va a configureDb con "+ userDb +" "+dbName)
        self.configureDb(userDb, dbName)

    def deleteDb(self,db,total=True):
        Database = self.resourcePath('/Databases/' + db)
        BlastDb = self.resourcePath('/BlastDb/' + db)
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
            shutil.rmtree(BlastDb)
        except:
            print("error deleting from BlastDb")
            pass
        try:
            shutil.rmtree(BlastResult)
        except:
            print("error deleting from BlastResult")
            pass
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

    def setCategoryToFilesInDb(self, db, folder, category):
        folderPath = self.resourcePath("/Databases/"+db+"/"+folder)
        categoriesFile = self.resourcePath("/Categories/"+db+".json")
        with open(categoriesFile, mode='r') as json_file:
            data = json.load(json_file)
        for bases, dirs, files in os.walk(folderPath):
            for file in files:
                #newJson = '{"'+os.path.basename(file.name)+'" : "'+self.categories[category]+'"}'
                data[file[:-3]] = category
        with open(categoriesFile, 'w') as f:  # writing JSON object
            json.dump(data, f)

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
#searcher.configureDb("BoLa")
#searcher.setCategoryToFilesInDb('BoLa', 'Mas_frecuentes', "ALTA")
#searcher.setCategoryToFilesInDb('BoLa', 'Menos_1%', "MEDIA")
#searcher.setCategoryToFilesInDb('BoLa', 'Menos_2%', "MEDIA")
#searcher.setCategoryToFilesInDb('BoLa', 'No_encontrados', "BAJA")

#searcher.searchHaplotypes()

#searcher.congifureDb()
#searcher.deleteSequence("BoLa", "DERB3_4501.fa")
#
#searcher.deleteSeq("BoLa","C:\Users\Paula\PycharmProjects\Haplotypes\BoLa\Mas_frecuentes\DRB3_2705.fa")
#searcher.addSeq("C:\Users\Paula\PycharmProjects\Haplotypes\BoLa\Mas_frecuentes","BoLa", "DRB3_2705",
                          #"GGAGTATTATAAGAGAGAGTGTCATTTCTTCAACGGGACCGAGCGGGTGCGGTTCCTGGACAGATGCTACACTAATGGAGAAGAGACCGTGCGCTTCGACAGCGACTGGGGCGAGTTCCGGGCGGTGACCGAGCTAGGGCGGCCGGACGCCGAGTACTGGAACAGCCAGAAGGACTTCCTGGAGGAGAGGCGGGCCGCGGTGGACAGGGTGTGCAGACACAACTACGGGGTCGTGGAGAGTTTCACTGTG")
#searcher.probarGlobalComparator()
#searcher.probarSimpleDbCreator()
#searcher.probarAmbiguousDbCreator()

