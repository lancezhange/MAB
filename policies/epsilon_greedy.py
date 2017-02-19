# coding=utf-8
import numpy as np
from policies.policy import Policy


class EpsilonGreedyPolicy(Policy, object):
    def __init__(self, args):
        Policy.__init__(self, args)
        self.anneal = args[2] > 0.0
        self.decay = args[1]

    def choose_arm(self):
        """选择臂"""
        if self.anneal:
            epsilon = self.get_epsilon()
        else:
            epsilon = self.decay
        if np.random.random() > epsilon:
            # Exploit
            return np.argmax(self.reward)
        else:
            # Explore
            return np.random.randint(self.n_bandits)

    def get_epsilon(self):
        """epsilon 衰减"""
        total = np.sum(self.counts)
        return float(self.decay) / (total + float(self.decay))
