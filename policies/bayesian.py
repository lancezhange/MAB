# coding=UTF-8 
# author: lancezhange


import numpy as np
from numpy.random import beta
from policies.policy import Policy


class BayesianPolicy(Policy, object):
    """又称 Thompson Sampling"""

    def __init__(self, args):
        Policy.__init__(self, args)
        # 记录每个臂的beta分布参数
        self.betaArgs = [[args[1], args[2]] for _ in range(self.n_bandits)]

    def choose_arm(self):
        """选择臂"""
        # 每个臂都至少被选择一次
        for arm in range(self.n_bandits):
            if self.counts[arm] == 0:
                return arm
        tmp = [beta(self.betaArgs[arm][0], self.betaArgs[arm][1]) for arm in range(self.n_bandits)]
        return np.argmax(tmp)

    def update(self, arm, reward):
        """更新收益
        :param reward: 收益
        :type arm: 选中的臂的下标
        """
        self.counts[arm] += 1
        n = self.counts[arm]
        value = self.reward[arm]
        # 平均收益
        new_value = value + (reward - value) / float(n)
        self.reward[arm] = new_value
        self.betaArgs[arm][0] += BayesianPolicy.identity(reward)  # 成功
        self.betaArgs[arm][1] += 1 - BayesianPolicy.identity(reward)

    @staticmethod
    def identity(x):
        if x > 0.0:
            return 1
        else:
            return 0
