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
        self.StockData = StockData
        self.stocks = np.zeros(self.StockNum)
        self.i = 1
        self.Promise = np.zeros((4,12))
        with open('RLFINAL.soc','rb') as f:
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
        YT,CT = NNStocks.L_model_forward(DataProcess.GetX(self.StockData[0,-101:-1],self.StockData[0,-1001:-1]),self.TATAParam)
        YV,CV = NNStocks.L_model_forward(DataProcess.GetX(self.StockData[1,-101:-1],self.StockData[1,-1001:-1]),self.VIParam)
        YK,CK = NNStocks.L_model_forward(DataProcess.GetX(self.StockData[2,-101:-1],self.StockData[2,-1001:-1]),self.KOTParam)
        YR,CR = NNStocks.L_model_forward(DataProcess.GetX(self.StockData[3,-101:-1],self.StockData[3,-1001:-1]),self.RILParam)
        X = np.hstack((np.hstack((np.hstack((YT,YV)),YK)),YR))
        return X



    def ReTrainStockModel(self):
        for j in range(0,10):
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

    def GetStocksOutlook(self):
        act = np.zeros(4)
        for j in range(0,4):
            if self.stocks[i] > 0:
                
