import gym
import numpy as np
from ppo_torch import Agent
import time

env = gym.make('CartPole-v0')

agent = Agent(n_actions=env.action_space.n,input_dims=env.observation_space.shape)
agent.load_models()
observation = env.reset()
done = False
score = 0
no_of_steps = 0

while not done:
    env.render()
    action, prob, val = agent.choose_action(observation)
    observationa, reward, done, info = env.step(action)
    score += reward
    no_of_steps += 1
    #agent.remember(observation, action, prob, val, reward, done)
    observation = observationa
    time.sleep(0.01)
print(score)
print(no_of_steps)
env.close()