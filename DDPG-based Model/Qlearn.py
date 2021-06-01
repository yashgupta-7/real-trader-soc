import getData



"""
The way I'm considering the state vector to be is to first have, the 150 element vector consisting of
data regarding the state of each stock, 5 elements each!

Then the next 30 would give me the integral amount of each stock owned

And then finally the balance in the last!


"""
class PreProcess :
    def __init__(self, File, entries = 10, _gamma = 0.25):
        self.Parser = Par(File,entries)
        self.data = self.Parser.GetData()
        self.XI = []
        self.YI = []
        self.vecf = []          #CompleteInfo
        self.pricf = []         #OnlyPriceInfo
        self.gamma = gamma
        self.muxi = []
        self.muyi = []
        GetStateVec()

    def GetStateVec(self):
        for x in self.data:
            z = np.array(x)
            L = []
            P = []
            for i in range(0,z.shape[0]):
                L += list(z[i,[3,8,9,10,11]])
                P += list(z[i,3])
            self.vecf.append(L)
            self.pricf.append(P)

    #The State is s at time t

    def TargetQ(self, s, t):
        Qi = 0
        sd = s
        td = t
        if t>=len(self.vecf)-1:
            return Qi
        else:
            for i in range(1,20):
                    if td == len(self.vecf)-1:
                        break
