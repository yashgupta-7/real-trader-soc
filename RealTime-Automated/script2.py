import main as m
import support as sp
import numpy as np

s = input('Input File name of Stock?')
#pos = int(input('Whats the position of the stock in the txt File?'))

#f = open('stocks.txt')
#comp = [float(x) for x in (f.readlines()[pos]).split(',')[1:]]
#print(len)
with open(s,'rb') as f:
    Prices = np.load(f)

#del comp[5]
It = Prices[1000:-1000]
X = []
Y = []
j = 0

for i in range(1000,Prices.shape[0]-750):
     print(i)
     X.append(m.GetX(Prices[(i-100):i],Prices[(i-1000):i]))
     Y.append(m.GetY(Prices[i-1],Prices[i:i+750]))

with open('X'+s,'wb') as f:
    np.save(f,np.array(X))

with open('Y'+s,'wb') as f:
    np.save(f,np.array(Y))
