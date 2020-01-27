import os
from Bio.Blast.Applications import NcbiblastnCommandline
import shutil
import sys
# ESTA CLASE HACE LA BUSQUEDA EN LA BASE DE DATOS PARA UNA DETERMINADA SECUENCIA GENERANDO UNA SALIDA BLASTQRESULT.
# PARA ESO RECIBE:
#       1: EL PATH DONDE ESTA LA BASE DE DATOS BLAST
#       2: DBNAME ES EL NOMBRE DEL ARCHIVO DE SECUENCIAS RESUMIDO QUE SE GENERA CON SIMPLEDBCREATOR
#       3: OUTPUTNAME ES EL NOMBRE DEL ARCHIVO DE SALIDA QUE GENERARA EL COMANDO NCBIBLASTCOMMANDLINE (RESULTADOS)
#       4: OUTPUTFORMAT ES FASTA (FORMATO DEL ARCHIVO DE SECUENCIAS RESUMIDO)
#       5: ORIGINALDBNAME TIENE EL NOMBRE DE LA BASE DE DATOS DE SECUENCIAS CON LA QUE SE TRABAJA
class SimpleBlast:
    def __init__(self, dbPath, dbName, outputName, outputFormat, outputPath, originalDbName=None, delete=False):
        self.dbName = dbName
        self.outputName = outputName
        self.outputFormat = outputFormat
        #self.projectPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if originalDbName is None:
            self.outputPath = self.resourcePath("/"+outputPath)
            self.dbPath = self.resourcePath("/"+dbPath)
        else:
            self.outputPath = self.resourcePath("/"+outputPath+"/"+originalDbName)
            self.dbPath = self.resourcePath("/"+dbPath +"/"+originalDbName)
        self.delete = delete

    def resourcePath(self,relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        output = base_path + relative_path
        return output

    def createFolder(self, newFolder):
        if not os.path.exists(newFolder):
            os.makedirs(newFolder)
        else:
            if (self.delete):
                try:
                    shutil.rmtree(newFolder)
                except:
                    for file in os.walk(newFolder):
                        os.close(file)
                    shutil.rmtree(newFolder)

                os.makedirs(newFolder)


    def align(self, query, queryName):
        self.alignPath = self.outputPath + "/"+queryName
        self.createFolder(self.alignPath)
        print("alignPath "+self.alignPath)
        print("query "+query)
        print("queryName "+queryName)
        i=0
        print("dbpath es "+self.dbPath)
        for bases, dirs, files in os.walk(self.dbPath):
            for file in files:
                # fileName es "secuencias.fasta" o salida.fasta
                #print("self.dbName "+self.dbName)
                #print("self.outputFormat "+self.outputFormat)
                #print("file "+file)
                fileName = self.dbName + "." + self.outputFormat
                fileArray = file.split('.')
                #print(fileArray)
                fileName = fileArray[0:len(fileArray)-1]
                if len(fileName)>1:
                    fileName='.'.join(fileName)
                else:
                    fileName = fileName[0]
                fileFormat = fileArray[len(fileArray)-1]
                #print("fileName "+fileName)
                #print("fileFormat "+fileFormat)
                #print(fileFormat+" "+self.outputFormat)
                if fileFormat == self.outputFormat:
                    self.dbName = file[:-6]
                    # ahora tengo que armar un archivo de salida para cada una de las bases de datos
                    dbPath =  bases + '/' + fileName
                    output =  self.alignPath+ '/'+queryName+"_"+str(i)
                    #print(output + "   " + dbPath)
                    # ya se tiene la base de datos creada. Crear el comando para buscar la secuencia query en la bd y generar salida
                    print(output)
                    blastnCline = NcbiblastnCommandline(query=query, db=dbPath, evalue=0.001, outfmt=5, out=output, word_size = 11)
                    print(blastnCline)
                    stdout, stderr = blastnCline()
                    i=i+1
