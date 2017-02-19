# coding=UTF-8 
# author: lancezhange

import numpy as np


class Policy(object):
    """
    policy 策略基类
    """
    def __init__(self, args):
        self.args = args
        self.n_bandits = int(args[0])  # 要求第一个参数必须是臂的个数！
        self.counts = [0] * self.n_bandits  # 记录每个臂的实验次数
        self.reward = [0.0] * self.n_bandits  # 记录每个臂的平均收益

    def choose_arm(self):
        """选择臂"""
        pass

    def update(self, arm, reward):
        """
        更新

        1. 该臂的摇动次数加一

        2. 该臂的平均收益更新
        """
        self.counts[arm] += 1
        n = self.counts[arm]
        value = self.reward[arm]
        # 平均收益
        new_value = value + (reward - value) / float(n)
        self.reward[arm] = new_value

    def print_result(self):
        """打印策略信息"""
        print "各臂的实验次数"
        print self.counts
        print "各臂获得的平均奖励"
        print self.reward
        print "总收益"
        print np.array(self.counts).dot(np.array(self.reward))
