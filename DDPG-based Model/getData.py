import pandas as pd
import numpy as np
import os

class Par:
    def __init__(self,File,entries):
        self.FileRead = open(File,'r')
        self.ent = entries
        self.dat = []

    def GetData(self):
        return self.dat

    def Read(self):
        i = 0
        j = 0
        k = 0
        dict = {}
        leg = []
        for x in self.FileRead.readlines():
            if i==0:
                leg = x.split(',')
                for y in leg:
                    dict[y] = []
            else:
                y = x.split(',')
                if y[1] != k:
                    k = y[1]
                    j+=1
                    self.dat.append(pd.DataFrame(dict))
                    for z in leg:
                        dict[z] = []

                for i in range(0,len(leg)):
                    dict[leg[i]].append(y[i])
                 dict[leg[1]].pop()
                 dict[leg[1]].append(j)

            i+=1
            if j > self.ent:
                break
