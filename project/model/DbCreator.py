import os

class DbCreator:
    def __init__(self, filesPath, newDb, dbName, outputFile, outputFormat):
        #self.projectPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # directorio donde se encuentran las secuencias individuales
        self.filesPath = self.resourcePath("/"+ filesPath)
        # directorio donde se creara la base de datos
        self.newDb = newDb
        #Nommbre de la base de datos seleccionada
        self.dbName = dbName
        # archivo intermedio usado para crear la base de datos
        self.outputFile = outputFile
        self.outputFormat = outputFormat

    def makeDb(self):
        pass


    def hasAllFilesWithExt(self, db, ext):
        for e in ext:
            if not any(fname.endswith(e) for fname in os.listdir(db)):
                return False
        return True

    def hasAllFiles(self,db):
        ext = []
        if os.name == 'nt':
            ext= ['.fasta', '.nhr', '.nin','.nog', '.nsd','.nsi', '.nsq' ]
        else:
            ext= ['.fasta', '.nhr', '.nin','.nog', '.not','.ntf', '.ndb', '.nos','.nsq', '.nto' ]
        return self.hasAllFilesWithExt(db, ext)