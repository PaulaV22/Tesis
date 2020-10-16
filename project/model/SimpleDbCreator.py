from Bio import SeqIO
import os
import subprocess
import sys
import shlex

from project.model import DbCreator as DBC
import project.model.SimpleBlast as SB
import shutil

# ESTA CLASE CREA UNA BASE DE DATOS BLAST A PARTIR DE ARCHIVOS DE SECUENCIAS.
# PARA ESO RECIBE:
#       1: EL PATH DONDE ESTAN LOS ARCHIVOS FASTA DE CADA SECUENCIA
#       2: EL NOMBRE DE LA NUEVA BASE DE DATOS BLAST A CREAR (Blastdb)
#       3: EL NOMBRE DE LA BASE DE DATOS SELECCIONADA (BOLA)
#       3: OUTPUTFILE ES EL NOMBRE DE UN ARCHIVO INTERMEDIO QUE REUNE TODAS LAS SECUENCIAS (CAMBIAR MAS REPRESENTATIVO)
#       4: OUTPUT FORMAT ES FASTA


class SimpleDbCreator(DBC.DbCreator):
    def __init__(self, filesPath, newDb, dbName, outputFile, outputFormat, ambiguous):
        DBC.DbCreator.__init__(self, filesPath, newDb, dbName, outputFile, outputFormat)
        self.ambiguous = ambiguous


    def resourcePath(self,relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        output = base_path + relative_path
        return output

    def createFolder(self, newFolder):
        if not os.path.exists(newFolder):
            print ("creo el directorio "+ newFolder)
            os.makedirs(newFolder)

    def getSequences(self, filePath, sequences):
        for seq_record in SeqIO.parse(filePath, self.outputFormat):
            seq = seq_record.seq
            sequences.append(seq_record)  # o seq?
        return sequences


    def saveSequencesInFile(self, path, sequences, outputFile= None):
        if outputFile is None:
            with open(path + "/" + self.outputFile + "." + self.outputFormat, "w+") as output_handle:
                SeqIO.write(sequences, output_handle, self.outputFormat)
        else:
            with open(path + "/" + outputFile + "." + self.outputFormat, "w+") as output_handle:
                SeqIO.write(sequences, output_handle, self.outputFormat)

    def makeBlastDb(self, directory):
        # formo "secuencias.fasta"
        outputName = self.outputFile + "." + self.outputFormat
        if outputName in os.listdir(directory):
            dbpath1 = directory + '/' + outputName
            dbpath2 = directory + '/' + self.outputFile
            dbpath1.replace(" ","_")
            dbpath2.replace(" ","_")

            #print 'secuencias.fasta esta en ' + dbpath1
            # ver este comando que es el que tiene problemas
            if os.name == 'nt':
                command = 'powershell.exe makeblastdb -in ' + dbpath1 + ' -out ' + dbpath2 + ' -parse_seqids -dbtype nucl'
                subprocess.Popen(command)
                print(subprocess.check_output(command))
            else:

                fullCommand = 'makeblastdb -in ' + dbpath1 + ' -out ' + dbpath2 + ' -parse_seqids -dbtype nucl'
                print("FULL COMMAND IS "+ fullCommand)
                command = subprocess.Popen(shlex.split(fullCommand))
                #command = subprocess.Popen(['makeblastdb', inParam, outputName,'-parse_seqids','-dbtype nucl'], stdout=subprocess.PIPE)
                output = command.communicate()

    def setFilesPath (self, filesPath):
        self.filesPath = filesPath

    def setOutputFile(self, file):
        self.outputFile = file

    def setOutputFormat(self, format):
        self.outputFormat= format

    def makeDb(self):
        dbPath = self.resourcePath('/'+self.newDb)
        dbPath= dbPath.replace(" ","_")
        self.createFolder(dbPath)
        # recorro los archivos y guardo las secuencias en un arreglo. Para cada directorio de las secuencias documentadas
        # creo el archivo secuencias.fasta para poder crear la base de datos en cada subdirectorio
        for bases, dirs, files in os.walk(self.filesPath):
            subdirectory = bases
            sequences = []
            array = subdirectory.split('/')
            print(array)
            self.user = array[len(array)-2]
            dbName = array[len(array)-1]

            newSubFolder = self.resourcePath("/"+self.newDb + "/" + self.user+ "/"+dbName)
            newSubFolder = newSubFolder.replace(" ", "_")

            # creo una subcarpeta para el subdirectorio correspondiente
            self.createFolder(newSubFolder)
            print("newSubFolder es " + newSubFolder)

            #print 'subfolder es ' + newSubFolder
            for file in os.listdir(subdirectory):
                filePath = subdirectory + '/' + file
                # si es un archivo fasta y no un directorio  --> ver, creo que hay una manera mas elegante de preguntar si es un archivo o directorio
                if os.path.isfile(filePath):
                    # obtengo las secuencias de cada archivo y la guardo en un arreglo de secuencias
                    sequences = self.getSequences(filePath, sequences)
                    # creo un archivo con las secuencias de ese subdirectorio
                    self.saveSequencesInFile(newSubFolder, sequences)
                    # con el archivo anterior puedo armar la base de datos en el subdirectorio
            self.makeBlastDb(newSubFolder)
            if not self.ambiguous:
                while (self.testDbFails(newSubFolder)):
                    self.makeBlastDb(newSubFolder)

    def testDbFails(self, db):
        print("A TESTEAR DB SIMPLE " + db)
        i = 0
        for f in os.listdir(db):
            if os.stat(db + "/" + f).st_size == 0:
                return True
            i = i + 1
        if i < 6:
            return True
        if not self.hasAllFiles(db):
            print("NO TIENE TODOS LOS ARCHIVOS")
            return True
        outputPath = "Test" + "/" + self.user +'/'+ self.dbName
        print("outputpath es " + outputPath)
        sb = SB.SimpleBlast(db, "salida", "salida", "fasta", outputPath)
        queryName = "queryTest.fa"
        queryPath = self.resourcePath("/" + queryName)
        try:
            print("va a alinear " + queryPath + " " + queryName)
            sb.align(queryPath, queryName)
        except:
            return True
        shutil.rmtree(self.resourcePath('/' + outputPath))
        return False