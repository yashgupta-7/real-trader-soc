'''
Grid World Solver with Policy iteration
Synchronous Sweep method
Finds Policy
Author: P Balasubramanian
Start Date: 16 May 2021
End Date: 17 May 2021
Estimated Time for Completion: 8 Hours

'''
import numpy as np


class Grid:

	def __init__(self, rows, columns, start, target, restricted_positions):

		#Initializing Variables
		self.rows = rows 
		self.columns = columns
		self.start = start
		self.target = target
		self.restricted_positions = restricted_positions

		# Initialising board
		self.board = np.zeros((self.rows, self.columns))

		# Setting start position on board
		self.board[self.start[0]][self.start[1]] = 1

		# Setting target position on board
		self.board[self.target[0]][self.target[1]] = 2

		# Setting restricted positions on board
		for (i, j) in self.restricted_positions:
			self.board[i][j] = -1

		# Initializing reward grid
		self.reward = np.ones((self.rows, self.columns))*(-1)
		self.reward[self.target[0]][self.target[1]] = 100

		for (i, j) in self.restricted_positions:
			self.reward[i][j] = -1000

		# Initialising state of system
		self.state = start


class Agent(Grid):

	def __init__(self, G):
		Grid.__init__(self,G.rows, G.columns, G.start, G.target, G.restricted_positions)

		# Initialising state-value grid to zero matrix
		self.value = np.zeros((self.board.shape[0], self.board.shape[1]))

		# policy is the probability distribution to multiple states performing actions
		# 0 is up, 1 is right, 2 is down, 3 is left

		self.policy = np.ones((4, self.board.shape[0], self.board.shape[1])) * 0.25
		self.policy[0][0] = 0
		self.policy[2][self.board.shape[0]-1] = 0

		for i in range(self.board.shape[0]):
			self.policy[3][i][0] = 0
			self.policy[1][i][self.board.shape[1]-1] = 0

		# up
		for i in range(1, self.board.shape[0]-1):
			self.policy[0][i][0] = self.policy[0][i][self.board.shape[1]-1] = (1.0/3)
		for i in range(self.board.shape[1]):
			if i==0 or i==(self.board.shape[1]-1):
				self.policy[0][self.board.shape[0]-1][i] = 0.5
			else:
				self.policy[0][self.board.shape[0] - 1][i] = (1.0/3)
		# down
		for i in range(1, self.board.shape[0]-1):
			self.policy[2][i][0] = self.policy[2][i][self.board.shape[1]-1] = (1.0/3)
		for i in range(self.board.shape[1]):
			if i == 0 or i == self.board.shape[1]-1:
				self.policy[2][0][i] = 0.5
			else:
				self.policy[2][0][i] = (1.0/3)
		# right
		for i in range(1, self.board.shape[1]-1):
			self.policy[1][0][i] = self.policy[1][self.board.shape[0]-1][i] = (1.0/3)
		for i in range(self.board.shape[0]):
			if i == 0 or i == self.board.shape[0]-1:
				self.policy[1][i][0] = 0.5
			else:
				self.policy[1][i][0] = (1.0/3)
		# left
		for i in range(1,self.board.shape[1]-1):
			self.policy[3][0][i]=self.policy[3][self.board.shape[0]-1][i]=(1.0/3)
		for i in range(self.board.shape[0]):
			if i==0 or i==self.board.shape[0]-1:
				self.policy[3][i][self.board.shape[1]-1]=0.5
			else:
				self.policy[3][i][self.board.shape[1]-1] = (1.0/3)

	def policy_evaluation(self,gamma):#computes and updates the value function based on policy defined
		# initializing updated value grid
		new_value = np.zeros((self.board.shape[0],self.board.shape[1]))
		for i in range(self.board.shape[0]):
			for j in range(self.board.shape[1]):
				if i!=0:
					new_value[i][j] += self.policy[0][i][j]*(self.reward[i-1][j]+gamma*self.value[i-1][j])

				elif j!=self.board.shape[1]-1:
					new_value[i][j] += self.policy[1][i][j]*(self.reward[i][j+1]+gamma*self.value[i][j+1])

				elif i!=self.board.shape[0]-1:
					new_value[i][j] += self.policy[2][i][j]*(self.reward[i+1][j]+gamma*self.value[i+1][j])

				elif j!=0:
					new_value[i][j] += self.policy[3][i][j]*(self.reward[i][j-1]+gamma*self.value[i][j-1])	

		return new_value			

	def policy_improvement(self):#calculates best strategy(policy) based on the evaluated value policy

		for i in range(self.policy.shape[1]):
			for j in range(self.policy.shape[2]):
				nxt_state_values_sum = 0
				if i < self.policy.shape[1]-1:
					nxt_state_values_sum += self.value[i+1][j]
				if j < self.policy.shape[2]-1:
					nxt_state_values_sum += self.value[i][j+1]
				if i > 0:
					nxt_state_values_sum += self.value[i-1][j]	
				if j > 0:
					nxt_state_values_sum += self.value[i][j-1]	

				# updating policy
				if i > 0:		
					self.policy[0][i][j] = self.value[i-1][j]/nxt_state_values_sum
				if j > 0:
					self.policy[3][i][j] = self.value[i][j-1]/nxt_state_values_sum	
				if i < self.policy.shape[1]-1:
					self.policy[2][i][j] = self.value[i+1][j]/nxt_state_values_sum
				if j < self.policy.shape[2]-1:
					self.policy[1][i][j] = self.value[i][j+1]/nxt_state_values_sum	

	def train(self,num_of_iterations,gamma):#To train the agent using DP techniques	
		
		for i in range(num_of_iterations):
			new_value = self.policy_evaluation(gamma)
			self.value = new_value
			self.policy_improvement()	
			
		self.disp_policy()
		self.disp_value()

	def disp_policy(self):	#display policy
		for i in range(self.policy.shape[1]):
			for j in range(self.policy.shape[2]):
				print("Policy in ",i,",",j,"is U: ",self.policy[0][i][j]," D: ",self.policy[2][i][j]," R: ",self.policy[1][i][j]," L: ",self.policy[3][i][j])

	def disp_value(self):	#display value grid
		print("Value Grid")
		print("----------------------------------------------------")
		
		for i in range(self.policy.shape[1]):
			X = "|"
			for j in range(self.policy.shape[2]):
				X+=str(self.value[i][j])
				X+="|"
			print(X)

		print("----------------------------------------------------")

# Getting Inputs about the Grid
Rows = int(input("Enter the number of rows in the Grid: "))	
Columns = int(input("Enter the number of columns in the Grid: "))
print("All rows and columns to be entered are 0 index.")

Start=[0,0]
Start[0] = int(input("Enter the row of starting position: "))
Start[1] = int(input("Enter the column of the starting position: "))

Target=[0,0]
Target[0] = int(input("Enter the row of the target position: "))	
Target[1] = int(input("Enter the column of the target position: "))

no_restricted_positions=int(input("Enter number of restricted positions: "))
restricted_positions = []
for i in range(no_restricted_positions):
	r = int(input('Enter the row of the {} th restricted position: '.format(i+1)))
	c = int(input('Enter the column of the {} th restricted position: '.format(i+1)))
	restricted_positions.append((r,c))

num_of_iterations = 100
gamma = 0.8

ans = input("Do you want to enter the number of iterations? [Y/N]")
if ans=='Y' or ans=='y':
	print("Enter a big number for the agent to train properly.")
	num_of_iterations = int(input("Enter num_of_iterations: "))

ans = input("Do you want to enter gamma? [Y/N]")
if ans=='Y' or ans=='y':
	print("Enter a number between 0 and 1")
	gamma = double(input("Enter gamma: "))

G = Grid(Rows,Columns,Start,Target,restricted_positions)
A = Agent(G)
A.train(num_of_iterations,gamma)
