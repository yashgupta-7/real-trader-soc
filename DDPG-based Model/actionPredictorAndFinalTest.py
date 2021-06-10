import NN
import numpy as np
import pandas as pd
import support as sp
import pickle
import random
import getData as gd

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
        return self.CurrOptimalAct

    def CheckFeasible(self,A):
        bal = 0
        bal+= self.CurrBalance
        #print(type(A))
        #print(A)
        for i in range(0,len(A)):
            #print(A[i])
            #print(A[i])
            #print(self.CurrState[150+i])
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

    def GenerateIntegral(self,A, prior):
        bal = 0
        bal += self.CurrBalance
        gotbal = 0
        couldhavegotbal = 0
        for i in range(0,len(A)):

            if A[i]<0:

                couldhavegotbal += sp.GetSingleTransacBC(self.CurrState[i*5],A[i])
                A[i] = round(A[i])
                if abs(A[i]) > self.CurrState[150+i]:
                    A[i] = -self.CurrState[150+i]
                bal+=sp.GetSingleTransacBC(self.CurrState[i*5],A[i])
                gotbal+=sp.GetSingleTransacBC(self.CurrState[i*5],A[i])

        if gotbal > 0.01:
            ratio = gotbal/couldhavegotbal
        else:
            ratio = 0.9

        for i in list(np.flip(np.argsort(np.array(prior)))):
            if A[i]>0:
                x = round(A[i]*ratio)
                if bal > sp.GetSingleTransacBC(self.CurrState[i*5],x):
                    A[i] = x
                    bal-= sp.GetSingleTransacBC(self.CurrState[i*5],x)
                else:
                    y = int(bal/(self.CurrState[i*5]*1.0012))
                    if y == 0:
                        A[i] = 0
                    else:
                        A[i] = y
                        bal-=sp.GetSingleTransacBC(self.CurrState[i*5],y)
        return A

    def GetAction(self):
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
            La[x]=(ston[g]/(self.CurrState[x*5]*1.0015))
            g+=1
        return La

    def OptimizeAction(self,A,V,S,t,learning_rate=0.1,beta1=0.9, beta2=0.999, epsilon=1e-8):
        # print(type(self.CurrState))
        # print(type(A))
        #print(len(self.CurrState))
        #print(A.shape)
        curr = np.expand_dims(np.array(self.CurrState+list(A)),axis = 0)
        #print(curr.shape)
        al, cac = NN.L_model_forward(curr,self.Parameters)
        #print(al)
        gra = NN.L_model_backwardAction(al,np.abs(al)*1000,cac)
        V = beta1*V + (1-beta1)*gra['dA1'][:,181:]
        VC = V/(1-np.power(beta1,t))
        S = beta2*S + (1-beta2)*np.power(gra['dA1'][:,181:],2)
        SC = S/(1-np.power(beta2,t))
        curr[:,181:] = curr[:,181:]-(learning_rate*(VC))/(np.sqrt(SC)+epsilon)
        return np.squeeze(curr[:,181:],axis = 0),V,S



    def CalculateOptimal(self) :
        for i in range(0,10):
            A = self.GetAction()
            self.CurrActionInp = [x for x in A]
            V,S = np.zeros((1,len(A))),np.zeros((1,len(A)))
            #print('Processing started for ',i,'th action.')
            j = 0
            inc = 0
            incPrev = 100
            val = 1000
            while val > 0.00004:
                A,V,S = self.OptimizeAction(A,V,S,j+1)
                inc = float(NN.L_model_forward(np.expand_dims(np.array(self.CurrState+list(A)),axis = 0),self.Parameters)[0])
                val = abs(inc-incPrev)/abs(incPrev)
                incPrev = inc
                j+=1
                #print(A)
                # if not self.CheckFeasible(list(A[0])):
                #     break
            #print('Processing ended for ',i,'th action.')
            A = self.GenerateIntegral(list(A),list(np.multiply(A-np.array(self.CurrActionInp),self.CurrState[0:150:5])))
            z = float(NN.L_model_forward(np.expand_dims(np.array(self.CurrState+A),axis = 0),self.Parameters)[0])
            if z > self.CurrOptimalInp:
                self.CurrOptimalInp = z
                self.CurrOptimalAct = A



A = actionPredict('paramFinal360.soc')

Pars = gd.Par('done_data.csv',100000000)
Pars.Read()
d = np.array(Pars.GetData())[2048:,:,[3,8,9,10,11]]
# print(d)
# print(d.shape)
T = []
for i in range(0,d.shape[0]):
    L = []
    for j in range(0,30):
        L+=list(d[i,j,:])
    T.append(L)

bal = 1000000
port = list(np.zeros(30))

for i in range(0,len(T)):

    X = [x for x in T[i]]
    X+=port
    X.append(bal)
    print('At the start of the ',i,'th TimeFrame, The Cumulative Profit was: ', (sp.GetEvaluation(np.array(X))-1000000)/10000.0, ' %' )
    act = A.RunFor(X)
    bal+=sp.GetBalanceChange(np.array(X[0:150:5]),np.array(act))
    port = list(np.array(port)+np.array(act))






#print(A.RunFor(X[-1,:]))
