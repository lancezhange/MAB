# coding=utf-8
# author: lancezhange

from testbed.environment import Environment

bandits_cfg = "bernoulli"
policies_cfg = ["ucb1",  "linucb", "softmax"]


env = Environment(bandits_cfg, policies_cfg)

scores = env.run(200, 500)

# 图画实验结果
env.plot_results(scores)
