import NN
import numpy as np
import pandas as pd
import support as sp
import pickle
import random

class actionPredict:
    def __init__(self,FileName):
        with open(FileName,'rb') as f:
            self.Parameters = pickle.load(f)
        self.CurrActionInp = []
        self.CurrOptimalInp = float('-inf')
        self.CurrOptimalAct = []
        self.CurrBalance = 0
        self.CurrState = []

    def RunFor(self, si):
        self.CurrState = list(si)
        self.CurrBalance = si[-1]
        self.CalculateOptimal()
        return self.OptimalAct

    def CheckFeasible(A):
        bal = self.CurrBalance
        for i in range(0,len(A)):
            if A[i]<0 and abs(A[i])<=self.CurrState[150+i]:
                bal+=sp.GetSingleTransacBC(self.CurrState[i*5],A[i])
            else:
                return False
        for i in range(0,len(A)):
            if A[i]>0:
                bal+=sp.GetSingleTransacBC(self.CurrState[i*5],A[i])

        if bal >= 0:
            return True
        else:
            return False

    def GenerateIntegral(A, prior):
        bal = self.CurrBalance
        for i in range(0,len(A)):
            if A[i]<0:
                A[i] = round(A[i])
                bal+=sp.GetSingleTransacBC(self.CurrState[i*5],A[i])
        cont = True
        for i in list(np.reverse(np.argsort(np.array(prior)))):
            if A[i]>0 and cont:
                x = round(A[i])
                if bal > sp.GetSingleTransacBC(self.CurrState[i*5],x)
                    A[i] = x
                    bal-= sp.GetSingleTransacBC(self.CurrState[i*5],x)
                else:
                    y = int(bal/(self.CurrState[i*5]*1.0012)
                    if y==0:
                        A[i] = 0
                    else:
                        A[i] = y
                        bal-=sp.GetSingleTransacBC(self.CurrState[i*5],y)
        return A

    def GetAction():
        La = np.zeros(30)
        bc = self.CurrState[-1]
        tod = []
        for t in range(0,30):
            a = random.randint(-1,1)
            if a == -1:
                bu = -random.random()*float(self.CurrState[150+t])
                bc+=sp.GetSingleTransacBC(self.CurrState[t*5],dk = bu)
                La[t]=bu
            elif a==1:
                tod.append(t)
        bcp = bc*random.random()
        ston = np.random.randint(0,1000,len(tod))
        ston = (ston/np.sum(ston))*bcp
        g = 0
        for x in tod:
            La[x]=(ston[g]/(self.CurrState[150+x]*1.0015))
            g+=1
        return La

    def GetOptimal(self) :
        for i in range(0,100):
            A = GetAction()
            
