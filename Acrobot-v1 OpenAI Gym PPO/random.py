import gym
env = gym.make('Acrobot-v1')
env.reset()

for _ in range(200):
    env.render()
    env.step(env.action_space.sample()) # take a random action
env.close()