# coding=UTF-8 
# author: lancezhange

import numpy as np
from policies.policy import Policy
import math


class LinUCBPolicy(Policy, object):
    """
    Linear Contextual Bandit Algorithm
    """

    def __init__(self, args):
        """
        我们人为生成一些上下文来模拟
        :param args: 臂个数参数，以及各个臂的穿越参数等
        """
        Policy.__init__(self, args)
        self.alpha = args[1]
        self.travel_args = args[2:]  # 穿越过来的臂均值参数
        self.d = 3  # 上下文维度
        self.A = np.array([np.identity(self.d) for _ in range(self.n_bandits)])
        self.b = np.array([np.zeros(self.d) for _ in range(self.n_bandits)])
        self.context = None

    def choose_arm(self):
        """选择臂"""
        self.context = np.array([self.get_context(i) for i in range(self.n_bandits)])
        p = [self.b[i].dot(self.A[i]).dot(self.context[i]) +
             self.alpha * math.sqrt(self.context[i].dot(np.linalg.inv(self.A[i])).dot(self.context[i]))
             for i in range(self.n_bandits)]
        return np.argmax(p)

    def update(self, arm, reward):
        """更新收益
        :param reward: 收益
        :type arm: 选中的臂的下标
        """
        Policy.update(self, arm, reward)
        self.b[arm] = self.b[arm] + reward * self.context[arm]
        self.context[arm].shape = (self.d, 1)
        self.A[arm] = self.A[arm] + self.context[arm].dot(np.transpose(self.context[arm]))

    def get_context(self, i):
        """
        生成上下文向量
        :param i: 臂的标，以便获取该臂的穿越参数生成上下文
        :return: 上下文向量
        """
        return [self.travel_args[i] + np.random.rand() for _ in range(self.d)]  # 线性变换
        # return [np.random.normal(self.travel_args[i], j + 1) for j in range(self.d)]  # 正态变换
