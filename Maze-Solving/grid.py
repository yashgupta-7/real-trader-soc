import numpy as np



class Grid:

    def __init__(self, n , m , target , start , blockades):

        self.grid = np.zeros((n,m),'<U1')
        for i in range(0,self.grid.shape[0]):
            for j in range(0,self.grid.shape[1]):
                self.grid[i][j] = '_'
        self._start = start
        self._target = target
        self.grid[start[0]][start[1]] = 'o'
        self.grid[target[0]][target[1]] = 'x'
        for (i,j) in blockades:
            self.grid[i][j] = 'z'


    def showgrid(self):
        print("----------------------------------------------------")
        for i in range(0,self.grid.shape[0]):
            X = "|"
            for j in range(0,self.grid.shape[1]):
                X.append(grid[i][j])
            print(X)

        print("----------------------------------------------------")



#0 means left, 1 means up, 2 means right and 3 means down
class Qlearn(Grid):

    def __init__(self, n,m,target, start, blockade, _gamma = 0.7, _alpha = 0.8):
        #print(len(blockades))
        Grid.__init__(self,n,m,target,start, blockade)
        self.Q = np.zeros((n,m,4))
        self.reward = np.zeros((n,m))
        self._n = n
        self._m = m
        self.gamma = _gamma
        self.alpha = _alpha
        self.numIter = 0
        self.Opt = ""
        for i in range(0,self.grid.shape[0]):
            for j in range(0,self.grid.shape[1]):
                self.Q[i][j][0] = 0
                self.Q[i][j][1] = 0
                self.Q[i][j][2] = 0
                self.Q[i][j][3] = 0
                if i==target[0] and j==target[1]:
                    self.reward[i][j] = 50
                if self.grid[i][j]=='z':
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
        RU = self.reward[1:n,:]
        RU = np.vstack((A,RU))
        RD = self.reward[0:n-1,:]
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
        if cando:
            self.Opt = op


    def Train(self,iterations):
        for i in range(iterations):
            if i % 10 == 0:
                self.OptPath()
                print('After {nu} iterations, The shortest path has length : {len}'.format(nu = i, len = len(self.Opt)))
            A = np.ones(n)
            A = float('-inf')*A
            A = np.expand_dims(A,1)
            QL = self.Q[:,:,1:m]
            QL = QL.max(axis = 0)
            QL = np.hstack((QL,A))
            QR = self.Q[:,:,0:m-1]
            QR = QL.max(axis = 0)
            QR = np.hstack((A,QR))
            A = np.ones(m)
            A = float('-inf')*A
            A = np.expand_dims(A,1)
            A = A.T
            QU = self.Q[:,0:n-1,:]
            QU = QU.max(axis = 0)
            QU = np.vstack((A,QU))
            QD = self.Q[:,1:n,:]
            QD = QD.max(axis = 0)
            QD = np.vstack((QD,A))
            QK = np.zeros((4,n,m))
            QK[0,:,:] = QL
            QK[1,:,:] = QU
            QK[2,:,:] = QR
            QK[3,:,:] = QD

            QK = self.R + (self.gamma)*QK

            self.Q = self.Q + (self.alpha)*(QK-self.Q)







N = 6#int(input("Enter the Number of Rows in your grid :"))
M = 6#int(input("Enter the Number of Columns in your grid :"))
si = 1#int(input("Enter the row of the starting point of your grid (0-based index):"))
sj = 1#int(input("Enter the column of the starting point of your grid (1-based index):"))
ei = 5#int(input("Enter the row of the target point of your grid (0-based index):"))
ej = 5#int(input("Enter the column of the target point of your grid (1-based index):"))

nb = 1#int(input("Enter the number of less-appropriate cells you wanna have in your grid :"))
block = []

for i in range(nb):
    ii = 2#int(input("Enter the row no. of the {num} th cell:".format(num = i+1)))
    ij = 3#int(input("Enter the coulmn no. of the {num} th cell:".format(num = i+1)))
    block.append((ii,ij))

myAgent = Qlearn(N,M,(ei,ej),(si,sj), block)
myAgent.Train(100)
