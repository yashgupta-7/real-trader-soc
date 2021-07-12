import numpy as np
import NNRL
import NNStocks
import support
import pickle
import DataProcess


class Portfolio:
    def __init__(self, initialBalance, stockData):
        self.bal = initialBalance
        self.StockNum = len(stockData)
        self.StockData = stockData
        self.stocks = np.zeros(self.StockNum)
        self.i = 1
        self.Promise = np.zeros((4,4))
        with open('RLFinal.soc','rb') as f:
            self.RLParam = pickle.load(f)
        with open('TATAFINAL.soc','rb') as f:
            self.TATAParam = pickle.load(f)
        with open('KOTFINAL.soc','rb') as f:
            self.KOTParam = pickle.load(f)
        with open('VIFINAL.soc','rb') as f:
            self.VIParam = pickle.load(f)
        with open('RILFINAL.soc','rb') as f:
            self.RILParam = pickle.load(f)
        self.VT,self.ST = NNStocks.initialize_adam(self.TATAParam)
        self.VR,self.SR = NNStocks.initialize_adam(self.RILParam)
        self.VK,self.SK = NNStocks.initialize_adam(self.KOTParam)
        self.VV,self.SV = NNStocks.initialize_adam(self.VIParam)

    def GetNetWorth(self):
        return self.bal+np.sum(self.stocks*self.StockData[:,-1])*0.9995

    def GetNextPrice(self, Prices):
        self.StockData = np.hstack((self.StockData,Prices))

    def SeeActionFeasible(self,action):
        bala = self.bal
        bala += np.sum(np.abs(action)*((action < 0).astype(float))*self.StockData[:,-1])*0.995
        if bala >= np.sum(np.abs(action)*((action > 0).astype(float))*self.StockData[:,-1])*1.005 :
            return True
        else:
            return False

    def GetOutLookVec(self):
        YT,CT = NNStocks.L_model_forward(DataProcess.GetX(self.StockData[0,-1001:-1]),self.TATAParam)
        YV,CV = NNStocks.L_model_forward(DataProcess.GetX(self.StockData[1,-1001:-1]),self.VIParam)
        YK,CK = NNStocks.L_model_forward(DataProcess.GetX(self.StockData[2,-1001:-1]),self.KOTParam)
        YR,CR = NNStocks.L_model_forward(DataProcess.GetX(self.StockData[3,-1001:-1]),self.RILParam)
        X = np.hstack((np.hstack((np.hstack((YT,YV)),YK)),YR))
        return X

    def RunAction(self,vec):
        self.stocks+=vec
        self.bal+=((np.sum(np.abs(vec)*((vec < 0).astype(float))*self.StockData[:,-1])*0.995)-(np.sum(np.abs(vec)*((vec > 0).astype(float))*self.StockData[:,-1])*1.005))

    def ReTrainStockModel(self):
        for j in range(0,10):
            print(self.StockData.shape)
            al,cal = NNStocks.L_model_forward(DataProcess.GetX(self.StockData[0,-2001:-1001]),self.TATAParam)
            Grad = NNStocks.L_model_backward(al,DataProcess.GetY(self.StockData[0,-1001],self.StockData[0,-1000:]),cal)
            self.TATAParam, self.VT,self.ST = NNStocks.update_parameters_with_adam(self.TATAParam,Grad,self.VT,self.ST,self.i)
            al,cal = NNStocks.L_model_forward(DataProcess.GetX(self.StockData[1,-2001:-1001]),self.VIParam)
            Grad = NNStocks.L_model_backward(al,DataProcess.GetY(self.StockData[1,-1001],self.StockData[1,-1000:]),cal)
            self.VIParam, self.VV,self.SV = NNStocks.update_parameters_with_adam(self.VIParam,Grad,self.VV,self.SV,self.i)
            al,cal = NNStocks.L_model_forward(DataProcess.GetX(self.StockData[2,-2001:-1001]),self.KOTParam)
            Grad = NNStocks.L_model_backward(al,DataProcess.GetY(self.StockData[2,-1001],self.StockData[2,-1000:]),cal)
            self.KOTParam, self.VK,self.SK = NNStocks.update_parameters_with_adam(self.KOTParam,Grad,self.VK,self.SK,self.i)
            al,cal = NNStocks.L_model_forward(DataProcess.GetX(self.StockData[3,-2001:-1001]),self.RILParam)
            Grad = NNStocks.L_model_backward(al,DataProcess.GetY(self.StockData[3,-1001],self.StockData[3,-1000:]),cal)
            self.RILParam, self.VR,self.SR = NNStocks.update_parameters_with_adam(self.RILParam,Grad,self.VR,self.SR,self.i)
            self.i+=1


    # For each stock, the promise vector contains of the time variable when it has to be re-considered(0), the buying price(1),
    # the profit concerned(2), and the max drawdown concerned with it!(3)
    def GetSellInfo(self,time):
        #1 in reas means selling because of loss, and 0 means selling because purpose is fulfilled!
        act = np.zeros(4)
        reas = np.zeros(4)
        for j in range(0,4):
            if self.stocks[j] > 0 and self.Promise[j,1] > 0:
                prof = ((self.StockData[j,-1]/self.Promise[j,1])-1.00)*100.0
                if prof/self.Promise[j,2] >= 0.9 and prof > 0.15:
                    act[j] = -self.stocks[j]
                    reas[j] = 0
                elif (prof/self.Promise[j,3]) >= 1.20:
                    act[j] = -self.stocks[j]
                    reas[j] = 1
                if self.Promise[j,0] <= time and (prof/self.Promise[j,2]) >= 0.5 and prof > 0.12:
                    act[j] = -self.stocks[j]
                    reas[j] = 0

        return np.array(act), reas

    def GetActionVector(self,X,act,reas,time):
        r,c = NNRL.L_model_forward(X,self.RLParam)
        J = []
        currbal = self.bal
        for j in range(0,4):
            if reas[j] < 1e-8:
                J.append(j)
            if act[j] < 0:
                currbal+=abs(act[j])*self.StockData[j,-1]

        L = []
        vec = [0,1.00,6.00,18.00,36.00,54.00,75.00]
        for j in J:
            x = X[0,j*12:(j+1)*12]
            takenProf = -1000
            promisevec = np.zeros(4)
            for i in range(1,7):
                if x[i-1] > 0.15 and x[i-1]/vec[i] > takenProf:
                    takenProf = x[i-1]/vec[i]
                    promisevec = np.array([time+int(10*vec[i]),self.StockData[j,-1],x[i-1],x[i+5]])
            if takenProf!=-1000:
                L.append((promisevec,j))
        sum = 0
        for l in L:
            sum+=r[0,l[1]]
        buylist = [0,0,0,0]
        for l in L:
            buylist[l[1]] = ((currbal*r[0,l[1]])/sum)/self.StockData[l[1],-1]
        buylist = np.array(buylist)
        while not self.SeeActionFeasible(buylist+act):
            buylist*=0.99
        for l in L:
            if buylist[l[1]] > 0:
                self.Promise[l[1],:] = np.array(l[0])
        return buylist+act

with open('TATA.npy','rb') as f:
    DT = np.load(f)[-1001:]
with open('VI.npy','rb') as f:
    DV = np.load(f)[-1001:]
with open('KOT.npy','rb') as f:
    DK = np.load(f)[-1001:]
with open('REL.npy','rb') as f:
    DR = np.load(f)[-1001:]

my = Portfolio(100000.00,np.vstack((np.vstack((np.vstack((DT,DV)),DK)),DR)))

with open('TATATEST.npy','rb') as f:
    DT = np.load(f)[-1001:]
with open('VITEST.npy','rb') as f:
    DV = np.load(f)[-1001:]
with open('KOTTEST.npy','rb') as f:
    DK = np.load(f)[-1001:]
with open('RELTEST.npy','rb') as f:
    DR = np.load(f)[-1001:]

Futures = np.vstack((np.vstack((np.vstack((DT,DV)),DK)),DR))

NetW = []

for i in range(0,Futures.shape[1]):
    a = my.GetOutLookVec()
    b,c = my.GetSellInfo(i)
    act = my.GetActionVector(a,b,c,i)
    my.RunAction(act)
    my.GetNextPrice(np.expand_dims(Futures[:,i],axis = 1))
    if my.StockData.shape[1] >=2002:
        my.ReTrainStockModel()
    NetW.append(my.GetNetWorth())
    print('After the ',i+1,'th Time Frame, Cumulative Profit Stands at: ', (NetW[len(NetW)-1]-100000.00)/1000.00,'%')
