import numpy as np



class Grid:

    def __init__(self, n , m , target , start , blockades):

        self.gridStat = np.zeros((n,m),'<U1')
        for i in range(0,self.gridStat.shape[0]):
            for j in range(0,self.gridStat.shape[1]):
                self.gridStat[i][j] = '_'
        self._start = start
        self._target = target
        self.gridStat[start[0]][start[1]] = 'O'
        self.gridStat[target[0]][target[1]] = 'X'
        for (i,j) in blockades:
            self.gridStat[i][j] = 'B'
        self.gridDyn = self.gridStat


    def showgrid(self):
        print("----------------------------------------------------")
        for i in range(0,self.gridDyn.shape[0]):
            X = "|"
            for j in range(0,self.gridDyn.shape[1]):
                X+=self.gridDyn[i][j]
                X+="|"
            print(X)

        print("----------------------------------------------------")



#0 means left, 1 means up, 2 means right and 3 means down
class Qlearn(Grid):

    def __init__(self, n,m,target, start, blockade, _gamma = 0.7, _alpha = 0.8):
        #print(len(blockades))
        Grid.__init__(self,n,m,target,start, blockade)
        self.Q = np.zeros((4,n,m))
        self.reward = np.zeros((n,m))
        self._n = n
        self._m = m
        self.gamma = _gamma
        self.alpha = _alpha
        self.numIter = 0
        self.Opt = ""
        for i in range(0,self.gridStat.shape[0]):
            for j in range(0,self.gridStat.shape[1]):
                self.Q[0][i][j] = 0
                self.Q[1][i][j] = 0
                self.Q[2][i][j] = 0
                self.Q[3][i][j] = 0
                if i==target[0] and j==target[1]:
                    self.reward[i][j] = 50
                if self.gridStat[i][j]=='B':
                    self.reward[i][j] = -1000

        A = np.ones(n)
        A = float('-inf')*A
        A = np.expand_dims(A,1)
        RL = self.reward[:,1:m]
        RL = np.hstack((RL,A))
        RR = self.reward[:,0:m-1]
        RR = np.hstack((A,RR))
        A = np.ones(m)
        A = float('-inf')*A
        A = np.expand_dims(A,1)
        A = A.T
        RU = self.reward[0:n-1,:]
        RU = np.vstack((A,RU))
        RD = self.reward[1:n,:]
        RD = np.vstack((RD,A))
        self.R = np.zeros((4,n,m))
        self.R[0,:,:] = RL
        self.R[1,:,:] = RU
        self.R[2,:,:] = RR
        self.R[3,:,:] = RD

    def OptPath(self):
        maxi = self._n*self._m
        op = ""
        it = 0
        cando = False
        i = self._start[0]
        j = self._start[1]
        while it<maxi :
            dec = self.Q[:,i,j].argmax(axis = 0)

            if self.Q[dec][i][j] == float('-inf'):
                break
            else:
                if dec==0:
                    j+=1
                elif dec==1:
                    i-=1
                elif dec==2:
                    j-=1
                else:
                    i+=1
                op+=str(dec)
            if i==self._target[0] and j==self._target[1]:
                cando = True
                break
            #print("i is {ii}, j is {jj}".format(ii = i, jj = j))
            if (i<0) or (i>=self._n) or (j<0) or (j>=self._m):
                #print("This!")
                break
        if cando:
            self.Opt = op


    def Train(self,iterations):
        for i in range(iterations):
            if i % 10 == 0:
                self.OptPath()
                print('After {nu} iterations, The shortest path has length : {len}'.format(nu = i, len = len(self.Opt)))
            A = np.ones(self._n)
            A = float('-inf')*A
            A = np.expand_dims(A,1)
            QL = self.Q[:,:,1:self._m]
            QL = QL.max(axis = 0)
            QL = np.hstack((QL,A))
            QR = self.Q[:,:,0:self._m-1]
            QR = QR.max(axis = 0)
            QR = np.hstack((A,QR))
            A = np.ones(self._m)
            A = float('-inf')*A
            A = np.expand_dims(A,1)
            A = A.T
            QU = self.Q[:,0:self._n-1,:]
            QU = QU.max(axis = 0)
            QU = np.vstack((A,QU))
            QD = self.Q[:,1:self._n,:]
            QD = QD.max(axis = 0)
            QD = np.vstack((QD,A))
            QK = np.zeros((4,self._n,self._m))
            QK[0,:,:] = QL
            QK[1,:,:] = QU
            QK[2,:,:] = QR
            QK[3,:,:] = QD

            QK = self.alpha*(self.R + (self.gamma)*QK)

            self.Q = self.Q*(1-self.alpha)
            self.Q = self.Q + QK


    def PrintCac(self):

        if len(self.Opt)==0:
            print("Training Incomplete!")
            return
        print("The Q-Values look like: ")
        print("The First Matrix denotes the values of Left, the second for Up, then right and then down")

        print(self.Q)

        print("The Way to proceed will be as follows: ")

        i = self._start[0]
        j = self._start[1]
        print("Presently the Grid Looks like: ")
        self.showgrid()
        k = 0
        op = self.Opt
        while i!=self._target[0] or j!=self._target[1]:

            if op[k]=='0':

                print("Then the Bot moved left from ({bi},{bj}) to ({bbi},{bbj})".format(bi = i,bj = j, bbi = i, bbj = j+1))
                self.gridDyn[i][j] = self.gridStat[i][j]
                if self.gridStat[i][j]=='O':
                    self.gridDyn[i][j] = '_'
                self.gridDyn[i][j+1] = 'O'
                j+=1

            elif op[k]=='1':
                print("Then the Bot moved up from ({bi},{bj}) to ({bbi},{bbj})".format(bi = i,bj = j, bbi = i-1, bbj = j))
                self.gridDyn[i][j] = self.gridStat[i][j]
                if self.gridStat[i][j]=='O':
                    self.gridDyn[i][j] = '_'
                self.gridDyn[i-1][j] = 'O'
                i-=1
            elif op[k]=='2':
                print("Then the Bot moved right from ({bi},{bj}) to ({bbi},{bbj})".format(bi = i,bj = j, bbi = i, bbj = j-1))
                self.gridDyn[i][j] = self.gridStat[i][j]
                if self.gridStat[i][j]=='O':
                    self.gridDyn[i][j] = '_'
                self.gridDyn[i][j-1] = 'O'
                j-=1
            else:
                print("Then the Bot moved down from ({bi},{bj}) to ({bbi},{bbj})".format(bi = i,bj = j, bbi = i+1, bbj = j))
                self.gridDyn[i][j] = self.gridStat[i][j]
                if self.gridStat[i][j]=='O':
                    self.gridDyn[i][j] = '_'
                self.gridDyn[i+1][j] = 'O'
                i+=1

            self.showgrid()
            k+=1





N = int(input("Enter the Number of Rows in your grid :"))
M = int(input("Enter the Number of Columns in your grid :"))
si = int(input("Enter the row of the starting point of your grid (0-based index):"))
sj = int(input("Enter the column of the starting point of your grid (0-based index):"))
ei = int(input("Enter the row of the target point of your grid (0-based index):"))
ej = int(input("Enter the column of the target point of your grid (0-based index):"))

nb = int(input("Enter the number of less-appropriate cells you wanna have in your grid :"))
block = []

for i in range(nb):
    ii = int(input("Enter the row no. of the {num} th cell:".format(num = i+1)))
    ij = int(input("Enter the coulmn no. of the {num} th cell:".format(num = i+1)))
    block.append((ii,ij))

g = 0.8
a = 0.001
ifg = input("Do you want to give a gamma(Deprication factor for Rewards) of your choice? Y/N")
if ifg=='Y':
    g = float(input("Gamma:"))
ifa = input("Do you want to give alpha (the learning rate) of your choice? Y/N")
if ifa=='Y':
    a = float(input("Alpha:"))

myAgent = Qlearn(N,M,(ei,ej),(si,sj), block, _gamma = g, _alpha = a)
numiter = 10000
ifi = input("Do you want to give number of iterations of Training your choice(default: 200)? Y/N")
if ifi=='Y':
    numiter = int(input("Number of Iterations:"))
myAgent.Train(iterations = numiter)
myAgent.PrintCac()
