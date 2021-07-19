#SoC 2021
# RL-Trader

This is the repository of programs and reports of the Summer of Code 2021 Module R(ea)L Trader where we make an Reinforcement Learning based Trading Agent to trade shares.

![](money.gif)

Description of my SoC'21 Coding Journey:<br><br>
I started my Reinforcement Learning journey by reading and understanding MDP's on the medium articles sent by my SoC mentors. It covered everything from properties of a Markov Decision Problem,Process, Markov Chains built its way throught the fundamental jargon such as states, actions, agent, environment, reward, episodic & non-terminating environments/games, transition probability, continuous & discrete action spaces, policy, optimal actions, policies and the Bellman, Bellman Optimality equation, Policy iteration, Value functions, Q-value, Q-Learning [9], Discounted Values & rewards right till methods to solve the Bellman Equation using Dynamic Programming methods to find the optimal policy.[6]<br><br>
This was my first time reading articles to understand a totally new concept, so I took help from additional resources on the internet such as the Coursera course 'Introduction to RL' by the University of Alberta [7] (which I completed by doing multiple coding assignments, quizzes on the bellman equations, value and policy iteration), RL lectures given by David Silver[4] (One of the chief RL Scientists at Google's DeepMind)(only watched 3 videos, the intro and MDP parts), few articles in Medium on Q-Learning, MDPS, Policy Gradients and a few other awesome youtube channels such as ArxivInsights[6] and CIS 522 - Deep Learning[5]. All these resources provided me with strong fundamentals in RL. <br><br>
I am quite fascinated by this field. The simplicity of formulation of the equation and the intuitive sense behind the equations (atleast at the start) and the power even these elementary architectures have to solve and 'play' in complex environments/simulations/games.The Alphago Documentary was another mindblowing RL documentary to watch.[15]<br><br>
After studying the basics, I went on to code and see some of these agents in action. I spent about 8 hours in May coding up a Value Iteration agent to navigate and solve the famous GridWorld (simply a maze) environment.( Code in repo) It turned out pretty well. I got the opportunity to code both the agent and the environment in that code which was quite awesome.<br><br>
Along with the above assignments, we were also told to study the basics of the stock market and do some paper trading in the US markets on an app called Invstr.[2] I am a person who is super into finance world, especially the stock markets after watching the movie 'The Big Short' and the brilliant series 'Scam 1992:The Harshad Mehta Story'. So owing to that curiosity I started my demat account and started investing (not trading) in good value stocks which I learnt to analyse after studying little from Zerodha's wonderful online tool called Varsity[16]. We were also sent links to Quantconnect and Blueshift, websites for testing out algos and learning computation and coding in the financial world.(I went through a few articles,strategies on QuantConnect and the intro to financial python in the same.[1],[18] <br><br>
During the next phase of the project, we were sent links from the mentors about an ensemble strategy to do RL Trading using previous data of stock high,low each day, Turbulence index and few other factors.[12] It has 3 different RL policy gradient methods namely PPO (Proximal Policy Optimisation),A2C (Advantage Actor-Critic) and DDPG (Deep Determininstic Policy Gradient). Since DDGP was implemented by fellow teammate Shubh, I decided to learn and implement the agent using PPO. I saw a few videos on the topic, went through the OpenAI (creators of PPO) documentation and the main paper on arxiv to get a good enough understanding for me to implement it.[10]<br><br>
To better understand neuralnets used in Actor-Critic networks such as in PPO, I did the 'Neural Networks and Deep Learning' course offered by Deeplearning.ai on Coursera and completed it.(Certificate Link [17]) The math and intuition behind how deep neuralnets work was given in the course along with many programming exercises to implement them from scratch with numpy or using the tensorflow framework.<br><br>
I also discovered OpenAI's gym and environments for RL agent testing around this time.[13] Iworked on my PPO model and used it a couple of Environments of the gym, namely CartPole-c0 and Acrobot-v1 which are 2 separate folders in this repo. I coded the agent using help from several videos and articles relating to PPO. I have used Pytorch framework to get myself acquinted with the ml framework predominantly used in academia, Pytorch. The resulting simulation video will be linked soon along with my main documentation.<br><br>
I have not completed my primary objective of building a RL trading agent, but I have learnt a lot, coded many systems from scratch, read a couple of papers and loooootsss of articles in this 2021 edition of SoC and will continue my RL quest...<br><br>
<br>
Resources Referred To:

[1]Python : https://www.w3schools.com/python/<br>
[2]Finance : Leagure on Invstr app to get started with paper trading<br>
[16]Zerodha's Varsity (https://zerodha.com/varsity/)<br>

Reinforcement Learning :<br>
[3]Overall reference : 'Reinforcement Learning:An Introduction' by Richard S. Sutton and Andrew G. Barto     <br>[Link]:https://web.stanford.edu/class/psych209/Readings/SuttonBartoIPRLBook2ndEd.pdf<br>
[4]RL Course by David Silver :<br> https://www.youtube.com/watch?v=2pWv7GOvuf0&list=PL7-jPKtc4r78-wCZcQn5IqyuWhBZ8fOxT&ab_channel=DeepMind<br>
[4]David Silver Course Slides : https://www.davidsilver.uk/teaching/<br>
[5]CIS 522 - Deep Learning's Reinforce Learning playlist:<br> https://www.youtube.com/watch?v=GJEL-QkT2yk&list=PLYgyoWurxA_8ePNUuTLDtMvzyf-YW7im2&index=6&ab_channel=CIS522-DeepLearning<br>
[6]Intro to RL (an Overview) : https://www.youtube.com/watch?v=JgvyzIkgxF0&ab_channel=ArxivInsights<br>

(MDPs) Medium Articles: <br>
[6]Part1 : https://towardsdatascience.com/introduction-to-reinforcement-learning-markov-decision-process-44c533ebf8da<br>
[6]Part2 : https://towardsdatascience.com/reinforcement-learning-markov-decision-process-part-2-96837c936ec3<br>
[6]Part3(Policy Iteration and Value Iteration) : https://towardsdatascience.com/reinforcement-learning-solving-mdps-using-dynamic-programming-part-3-b53d32341540<br>

MDPs and Techniques to Solve the Bellman Equation:<br>
[7]Fundamentals of Reinforcement Learning in Coursera : https://www.coursera.org/learn/fundamentals-of-reinforcement-learning<br>
[8]Policy Classes OF RL : https://towardsdatascience.com/the-four-policy-classes-of-reinforcement-learning-38185daa6c8a<br>

Q-Learning :<br>
[9]Grid world problem : https://towardsdatascience.com/implement-grid-world-with-q-learning-51151747b455<br>
[9]Tic-Tac-Toe : https://towardsdatascience.com/how-to-play-tic-tac-toe-using-reinforcement-learning-9604130e56f6<br>

PPO(Proximal Policy Optimization):<br>
[10]https://openai.com/blog/openai-baselines-ppo/<br>
[10]paper: https://arxiv.org/pdf/1707.06347.pdf<br>
[10]https://www.youtube.com/watch?v=5P7I-xPq8u8&ab_channel=ArxivInsights<br>

Actor-Critic:<br>
[11]https://www.youtube.com/watch?v=w_3mmm0P0j8&ab_channel=SirajRaval<br>
[17]https://coursera.org/share/f46591937f0e1a336b037b4269f7731b

Ensemble trading Agent:<br>
[12]https://towardsdatascience.com/deep-reinforcement-learning-for-automated-stock-trading-f1dad0126a02<br>
[12]paper : https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3690996<br>
[12]https://github.com/AI4Finance-LLC/Deep-Reinforcement-Learning-for-Automated-Stock-Trading-Ensemble-Strategy-ICAIF-2020<br>

OpenAI Gym:<br>
[13]https://gym.openai.com/docs/<br>

Extra RL Videos I found super interesting:<br>
[14]https://www.youtube.com/watch?v=Lu56xVlZ40M&ab_channel=TwoMinutePapers<br>
[14]https://www.youtube.com/watch?v=pQA8Wzt8wdw&ab_channel=TwoMinutePapers<br>
https://www.youtube.com/watch?v=a8Bo2DHrrow&ab_channel=Yosh<br>
[15]https://www.youtube.com/watch?v=WXuK6gekU1Y&ab_channel=DeepMind<br>
[14]https://www.youtube.com/watch?v=tfb6aEUMC04&ab_channel=TwoMinutePapers<br>

Quant Trading :<br>
[18]Intro to financial python : https://www.quantconnect.com/tutorials/tutorial-series/introduction-to-financial-python<br>
[18]For coding and backtesting strategies : Blueshift(https://blueshift.quantinsti.com/) or Quantconnect(https://www.quantconnect.com)<br>
[18]Regression based Strategies : https://www.quantconnect.com/tutorials/strategy-library<br>

Note: The description part was wriiten on th 19th and 20th of July. The codes were completed before the deadline and submitted making some changes.
