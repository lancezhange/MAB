# coding=UTF-8 
# author: lancezhange

import numpy as np
from policies.policy import Policy
import math


class EXP3Policy(Policy, object):
    """
    Exponential-weight algorithm for Exploration and Exploitation

    权重和随机性之间，用参数 :math:`\gamma` 协调

    see more: `Adversarial Bandits and the Exp3 Algorithm <https://jeremykun.com/2013/11/08/adversarial-policies-and-the-exp3-algorithm/>`_
    """

    def __init__(self, args):
        Policy.__init__(self, args)
        self.gamma = args[1]
        self._weights = np.array([1] * self.n_bandits)
        self._probs = None

    def choose_arm(self):
        """选择臂"""
        self._probs = self._weights * (1 - self.gamma) / self._weights.sum() + self.gamma / self.n_bandits
        cumulative_probs = 0.0
        r = np.random.random()
        for i in range(len(self._probs)):
            prob = self._probs[i]
            cumulative_probs += prob
            # 利用累积概率进行按概率分配
            if cumulative_probs > r:
                return i
        return len(self._probs) - 1

    def update(self, arm, reward):
        Policy.update(self, arm, reward)
        ratio = math.exp(self.gamma * reward / (self.n_bandits * self._probs[arm]))
        # todo 权重会越来越大？
        self._weights[arm] *= ratio
