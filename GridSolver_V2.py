'''
Grid World Solver with Policy iteration: Version 2
Author: P Balasubramanian
'''
import numpy as np

def convert(list):
    return tuple(list)

# user given global variables
BOARD_ROWS = int(input("Enter the number of rows in the Grid: "))
BOARD_COLS = int(input("Enter the number of columns in the Grid: "))

print("All rows and columns to be entered are 0 index.")
WIN_STATE = [0, 0]
LOSE_STATE = []
START = [0, 0]

START[0] = int(input("Enter the row of starting position: "))
START[1] = int(input("Enter the column of the starting position: "))

WIN_STATE[0] = int(input("Enter the row of the target position: "))
WIN_STATE[1] = int(input("Enter the column of the target position: "))

DETERMINISTIC = True
no_restricted_positions = int(input("Enter number of restricted positions: "))
for i in range(no_restricted_positions):
    r = int(input('Enter the row of the {} th restricted position: '.format(i + 1)))
    c = int(input('Enter the column of the {} th restricted position: '.format(i + 1)))
    LOSE_STATE.append((r, c))

LOSE_STATE = convert(LOSE_STATE)
START = convert(START)
WIN_STATE = convert(WIN_STATE)
print(LOSE_STATE)

class State:
    def __init__(self, state=START):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        print(self.board.shape)
        for (i,j) in LOSE_STATE:
            self.board[i, j] = -1
        self.state = state
        self.isEnd = False
        self.determine = DETERMINISTIC

    def giveReward(self):
        if self.state == WIN_STATE:
            return 5
        elif self.state in LOSE_STATE:
            return -5
        else:
            return -1

    def isEndFunc(self):
        if (self.state == WIN_STATE) or (self.state in LOSE_STATE):
            self.isEnd = True

    def nxtPosition(self, action):
        
        if self.determine:
            if action == "up":
                nxtState = (self.state[0] - 1, self.state[1])
            elif action == "down":
                nxtState = (self.state[0] + 1, self.state[1])
            elif action == "left":
                nxtState = (self.state[0], self.state[1] - 1)
            else:
                nxtState = (self.state[0], self.state[1] + 1)
            # if next state legal
            if (nxtState[0] >= 0) and (nxtState[0] <= (BOARD_ROWS -1)):
                if (nxtState[1] >= 0) and (nxtState[1] <= (BOARD_COLS -1)):
                    if nxtState != (1, 1):
                        return nxtState
            return self.state

    def showBoard(self):
        self.board[self.state] = 1
        for i in range(0, BOARD_ROWS):
            print('-----------------')
            out = '| '
            for j in range(0, BOARD_COLS):
                if self.board[i, j] == 1:
                    token = '*'
                if self.board[i, j] == -1:
                    token = 'z'
                if self.board[i, j] == 0:
                    token = '0'
                out += token + ' | '
            print(out)
        print('-----------------')


# Agent of player

class Agent:

    def __init__(self):
        self.states = []
        self.actions = ["up", "down", "left", "right"]
        self.State = State()
        self.lr = 0.2
        self.exp_rate = 0.3

        # initial state reward
        self.state_values = {}
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                self.state_values[(i, j)] = 0  # set initial value to 0

    def chooseAction(self):
        # choose action with most expected value
        mx_nxt_reward = 0
        action = ""

        if np.random.uniform(0, 1) <= self.exp_rate:
            action = np.random.choice(self.actions)
        else:
            # greedy action
            for a in self.actions:
                # if the action is deterministic
                nxt_reward = self.state_values[self.State.nxtPosition(a)]
                if nxt_reward >= mx_nxt_reward:
                    action = a
                    mx_nxt_reward = nxt_reward
        return action

    def takeAction(self, action):
        position = self.State.nxtPosition(action)
        return State(state=position)

    def reset(self):
        self.states = []
        self.State = State()

    def play(self, rounds=10):
        i = 0
        while i < rounds:
            # to the end of game back propagate reward
            if self.State.isEnd:
                # back propagate
                reward = self.State.giveReward()
                # explicitly assign end state to reward values
                self.state_values[self.State.state] = reward  # this is optional
                print("Game End Reward", reward)
                for s in reversed(self.states):
                    reward = self.state_values[s] + self.lr * (reward - self.state_values[s])
                    self.state_values[s] = round(reward, 3)
                self.reset()
                i += 1
            else:
                action = self.chooseAction()
                # append trace
                self.states.append(self.State.nxtPosition(action))
                print("current position {} action {}".format(self.State.state, action))
                # by taking the action, it reaches the next state
                self.State = self.takeAction(action)
                # mark is end
                self.State.isEndFunc()
                print("nxt state", self.State.state)
                print("---------------------")

    def showValues(self):
        for i in range(0, BOARD_ROWS):
            print('----------------------------------')
            out = '| '
            for j in range(0, BOARD_COLS):
                out += str(self.state_values[(i, j)]).ljust(6) + ' | '
            print(out)
        print('----------------------------------')


if __name__ == "__main__":
    ag = Agent()
    ag.play(50)
    print(ag.showValues())