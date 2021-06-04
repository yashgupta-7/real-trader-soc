import math
import numpy as np

#The s given here is the entire state vector and the a given belongs to Z^30


def GetSingleTransacBC(p,dk,transac = 0.001):
    #print(type(p))
    return (p*(-dk)) - abs(p*dk*transac)

def GetBalanceChange(p,dk,transac = 0.001):
    return np.sum((p)*(-dk)) - np.sum(abs(p*dk)*transac)

# The Single Reward Calculation Function is used to get whether or not, it should be a nice idea to
# sacrifice a loss-producing or absymally profit producing stock for something else, that is why we
#double the transaction charge, so that suppose on the next turn, it so happens that it becomes
#a very attractive bet to place our money here, then we could do that without spending too much
#as transaction fee.

def SingleRewardCalc(pa,pb,ki,kf,transac=0.001):
    return GetSingleTransacBC(pb,dk = kf-ki)+(kf*pa)-(ki*pb)

def GetReward(pb,pa,ki,kf,transac = 0.001):
    return GetBalanceChange(pb,transac,kf-ki) + np.sum((kf*pa)-(ki*pb))

def GetEvaluation(si):
    return np.sum(np.multiply(si[0:150:5],si[150:180]))*0.999 + si[-1]
