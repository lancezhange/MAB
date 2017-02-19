# coding=UTF-8 
# author: lancezhange

import numpy as np
from policies.policy import Policy
import math


class UCB1Policy(Policy, object):
    def __init__(self, args):
        Policy.__init__(self, args)

    def choose_arm(self):
        """选择臂"""
        # 确保每个臂都至少被摇过一次
        for arm in range(self.n_bandits):
            if self.counts[arm] == 0:
                return arm

        ucb = np.zeros(self.n_bandits)
        total_counts = sum(self.counts)
        for arm in range(self.n_bandits):
            confidence = math.sqrt((2 * math.log(total_counts)) / float(self.counts[arm]))
            ucb[arm] = self.reward[arm] + confidence
        return np.argmax(ucb)