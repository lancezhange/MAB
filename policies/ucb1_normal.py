# coding=UTF-8 
# author: lancezhange


import numpy as np
from policies.policy import Policy
import math


class UCB1NormalPolicy(Policy, object):
    """
    应该哪里有错，结果波动很大
    """
    def __init__(self, args):
        Policy.__init__(self, args)
        self.squared_reward = [0.0] * self.n_bandits

    def choose_arm(self):
        """选择臂"""
        # 确保每个臂都被摇过足够次数
        pull_count = sum(self.counts)+1
        mini_count = UCB1NormalPolicy.mini_pull(pull_count)

        for arm in range(self.n_bandits):
            if self.counts[arm] <= mini_count:
                return arm
        tmp = [0.0]*self.n_bandits
        for arm in range(self.n_bandits):
            reward = self.reward[arm]
            pulled = self.counts[arm]
            sr = self.squared_reward[arm]
            nominator = 16*(sr-pulled*reward*reward)*math.log(pull_count-2)
            denominator = pulled*(pulled-1)
            if nominator <= 0.0 or denominator <= 0.0:
                tmp[arm] = 0.0
                continue
            tmp[arm] = reward + math.log(nominator/denominator)
        return np.argmax(tmp)

    def update(self, arm, reward):
        """更新收益"""
        self.counts[arm] += 1
        n = self.counts[arm]
        value = self.reward[arm]
        # 平均收益
        new_value = value + (reward - value) / float(n)
        self.reward[arm] = new_value
        self.squared_reward[arm] += reward**2

    @staticmethod
    def mini_pull(n):
        return math.ceil(8 * math.log(n))
