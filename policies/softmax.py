# coding=UTF-8 
# author: lancezhange

import numpy as np
from policies.policy import Policy
import math


class SoftmaxPolicy(Policy, object):
    """
    softmax 算法(也有称为 Hedge 算法的)
    每次选择 softmax(收益)最大
    """
    def __init__(self, args):
        Policy.__init__(self, args)
        self.temperature = args[1]  # 降火参数，温度越高，分子越随机，成为气体；低温的时候有序排列，成为固体
        self.anneal = args[2] > 0.0

    def choose_arm(self):
        """选择臂"""
        probs = self.get_probs()
        cumulative_probs = 0.0
        r = np.random.random()
        for i in range(len(probs)):
            prob = probs[i]
            cumulative_probs += prob
            # 利用累积概率进行按概率分配
            if cumulative_probs > r:
                return i
        return len(probs) - 1

    def get_probs(self):
        """返回 softmax 概率"""
        if self.anneal:
            self.annealing()
        z = sum([math.exp(v / self.temperature) for v in self.reward])
        probs = [math.exp(v / self.temperature) / z for v in self.reward]
        return probs

    def annealing(self):
        """降火方法，注意不要让温度过高"""
        t = sum(self.counts) + 1
        self.temperature = max(100, 1 / math.log(t + 0.0000001))

