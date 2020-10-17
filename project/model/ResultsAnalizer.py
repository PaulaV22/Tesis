from __future__ import division
import os
from Bio import SearchIO
from Bio import AlignIO
import sys
import json

class ResultsAnalizer():

    def __init__(self, resultsPath, dbName, ambiguo):
        # recibe (FinalResult, BoLa o Prueba2)
      #  self.projectPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.resultsPath = self.resourcePath("/"+resultsPath)
        self.dbName = dbName
        self.resultFiles = self.resourcePath("/"+resultsPath+"/"+dbName)
        self.ambiguo= ambiguo

    def resourcePath(self,relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        output = base_path + relative_path
        return output

    def getStandarName(self,id):
        id = id.replace("_", "*")
        id = id.replace("/", "-")
        return id

    def getComplementary(self, id):
        seq1 = id.split('-')[0]
        seq2 = id.split('-')[1]
        output = seq2+"-"+seq1
        return output

    def getSimilarSequences(self, name, number=None):
        self.resultFiles = self.resultFiles + "/"+name
        i = 0
        sequences = dict()
        for bases, dirs, files in os.walk(self.resultFiles):
            for file in files:
                outputName = bases + "/" + file
                result = SearchIO.read(outputName, "blast-xml")
                for hits in result:
                    i = i+1
                    hsp = hits[0]
                    print("HSP")
                    print(hsp)
                    id = hsp.hit.id
                    score = hsp.bitscore
                    evalue = hsp.evalue
                    positives = hsp.pos_num
                    align_length = hsp.aln_span
                    percent = float("{0:.3f}".format(positives/align_length))
                    #weight = self.getWeight(id,sequencesCategories, file)
                    complementary =""
                    if self.ambiguo:
                        id = self.getStandarName(id)
                        complementary = self.getComplementary(id)
                    alignment = hsp.fragment.aln
                    if not (complementary in sequences.keys()):
                        #sequences[id] = [score * weight, evalue, positives, align_length, percent*weight]
                        sequences[id] = [score, evalue, positives, align_length, percent,alignment.format("fasta"),
                                         hsp.query_start, hsp.hit_start]

        n = 0
        salida = []

        #sort by e-value
        s = sorted(sequences.items(), key=lambda item: item[1][2], reverse=True)
        #sort by similarity
        s = sorted(s, key=lambda item: item[1][4], reverse=True)

       # for key, value in sorted(sequences.items(), key=lambda item: item[1][4], reverse=True):
        for key, value in s:
            if (n<int(number)):
                value.insert(0, key)
                print(value)
                data = {'id' :value[0], 'score':value[1], 'evalue':value[2], 'similarity':value[5],
                        'alignment':value[6], 'queryStart':value[7], 'hitStart':value[8]}
                salida.append(data)
            n = n +1
        #print(salida)
        salidaJson = json.dumps(salida)
        #print(number)
        return salidaJson

