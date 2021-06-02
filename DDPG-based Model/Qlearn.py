import getData
from support import GetBalanceChange,GetSingleTransacBC,GetReward,SingleRewardCalc
import random
import numpy as np
import pandas as pd

#In general, We store our data as lists, but when it comes to passing them to other functions for manipulating purposes,
# We'll prefer Numpy Arrays.



"""
The way I'm considering the state vector to be is to first have, the 150 element vector consisting of
data regarding the state of each stock, 5 elements each!

Then the next 30 would give me the integral amount of each stock owned

And then finally the balance in the last!


"""


class PreProcess :
    def __init__(self, File, entries = 10, _gamma = 0.25):
        self.Parser = getData.Par(File,entries)
        self.Parser.Read()
        print('Done')
        self.data = self.Parser.GetData()
        self.XI = []
        self.AI = []
        self.YI = []
        self.vecf = []          #CompleteInfo
        self.pricf = []         #OnlyPriceInfo
        self.gamma = _gamma


    def GetStateVec(self):
        print(self.data[0])
        for x in self.data:
            z = np.array(x)
            L = []
            P = []
            #print(z.shape)
            for i in range(0,z.shape[0]):
                L += list(z[i,[3,8,9,10,11]])
                P.append(z[i,3])
            #print(len(L))
            #print(len(P))
            self.vecf.append(L)
            self.pricf.append(P)

    #The State is s at time t
    def CreateDataSet(self):

        for i in range(0,len(self.vecf)-21):
            sd = []
            for g in range(0,30):
                #print('i = ',i,', g = ',g,', shape of vecf is ', len(self.vecf),len(self.vecf[i]))
                sd+=self.vecf[i][g]
            for j in range(0,5):
                sd+=list(np.random.randint(0,1000,30))
                for k in range(0,5):
                    sd.append(random.random()*1000000)
                    for z in range(0,10):
                        La = np.zeros(30)
                        bc = sd[-1]
                        tod = []
                        for t in range(0,30):
                            a = random.randint(-1,1)
                            if a == -1:
                                bu = -int(random.random()*float(sd[150+t]))
                                bc+=GetSingleTransacBC(self.pricf[i][t],dk = bu)
                                La[t]=bu
                            elif a==1:
                                tod.append(t)
                        bcp = bc*random.random()
                        ston = np.random.randint(0,1000,len(tod))
                        ston = (ston/np.sum(ston))*bcp
                        g = 0
                        for x in tod:
                            La[x]=int(ston[g]/self.pricf[i][x])
                            g+=1
                        self.XI.append(sd)
                        self.AI.append(La)
                        snext = []
                        for g in range(0,30):
                            snext+=self.vecf[i+1][g]
                        snext += list(np.array(sd[150:180])+np.array(La))
                        snext.append(sd[-1]+GetBalanceChange(self.pricf[i],dk = La))
                        self.yi.append(TargetQ(snext,i+1))

        with open('XI.npy','wb') as f:
            np.save(f,np.array(self.XI))
        with open('YI.npy','wb') as f:
            np.save(f,np.array(self.YI))
        with open('AI.npy','wb') as f:
            np.save(f,np.array(self.AI))




    def TargetQ(self, s, t):
        Qi = 0
        sd = s
        td = t
        fact = self.gamma
        if t>=len(self.vecf)-1:
            return Qi
        else:
            for i in range(1,20):
                if td == len(self.vecf)-1:
                    break
                K = np.zeros(30)
                StockDiff = (np.array(self.pricf[td+1])-np.array(self.pricf[td]))/np.array(self.pricf[td])
                bc = 0
                for i in range(150,180):
                    if sd[i] > 0.5  and SingleRewardCalc(self.pricf[td][(i-150)],self.pricf[td+1][(i-150)],sd[i],0) > 0 :
                        K[i-150] = -sd[i]
                        bc+=GetSingleTransacBC(self.pricf[td][(i-150)],dk = -sd[i])

                li = np.argsort(StockDiff,kind = 'mergesort')
                maxi = li[len(li)-1]
                if StockDiff[maxi] > 0.003 :

                    L = []
                    for i in range(0,len(li)-1):
                        if int(sd[150+li[i]]) > 0 :
                             L.append(li[i])
                    Lf = []
                    ammo = sd[-1]+bc
                    for i in range(0,len(L)):
                        if SingleRewardCalc(self.pricf[td][maxi],self.pricf[td+1][maxi],0,GetSingleTransacBC(self.pricf[td][L[i]],dk = -sd[150+L[i]])/((1.002)*self.pricf[td][maxi]))-SingleRewardCalc(self.pricf[td][L[i]],self.pricf[td+1][L[i]],sd[150+L[i]],sd[150+L[i]])+SingleRewardCalc(self.pricf[td][L[i]],self.pricf[td+1][L[i]],sd[150+L[i]],0) > 0:
                            Lf.append(L[i])
                            ammo+=GetSingleTransacBC(self.pricf[td][L[i]],dk = -sd[150+L[i]])
                        else:
                            break
                    ammo = int(ammo/((1.001)*self.pricf[td][maxi]))*(1.001)*self.pricf[td][maxi]
                    amm = 0
                    buy = 0
                    for i in range(0,len(Lf)):
                        if amm+GetSingleTransacBC(self.pricf[td][L[i]],dk = -sd[150+Lf[i]]) < ammo:
                            K[Lf[i]] = -sd[150+Lf[i]]
                            bc+=GetSingleTransacBC(self.pricf[td][L[i]],dk = -sd[150+Lf[i]])
                            amm+=GetSingleTransacBC(self.pricf[td][L[i]],dk = -sd[150+Lf[i]])
                        else:
                            num = int((ammo-amm)/(1.001*self.pricf[td[Lf[i]]]))
                            K[Lf[i]] = -num
                            bc+=GetSingleTransacBC(self.pricf[td][L[i]],dk = -num)
                            amm+=GetSingleTransacBC(self.pricf[td][L[i]],dk = -num)
                    K[maxi] = int((sd[-1]+bc)/((1.001)*self.pricf[td][maxi]))
                    bc+=GetSingleTransacBC(self.pricf[maxi],dk = K[maxi])

                Qi+=fact*GetReward(np.array(self.pricf[td]),np.array(self.pricf[td+1]),sd[150:180],sd[150:180]+np.array(K))
                fact*=self.gamma
                sd[-1]+=bc
                L = []
                for i in range(0,30):
                    L+=self.vecf[td+1][i]
                sd[0:150] = np.array(L)
                sd[150:180] += np.array(K)
                td+=1
            return Qi


X = PreProcess('done_data.csv',entries = 9000000)
X.GetStateVec()
X.CreateDataSet()
