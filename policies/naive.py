# coding=UTF-8 
# author: lancezhange

import numpy as np
from policies.policy import Policy


class NaivePolicy(Policy, object):
    """
    又名  Explore-first 算法

    每个臂先都摇几次，然后选择收益最大的臂固定下来一直摇
    """
    def __init__(self, args):
        Policy.__init__(self, args)
        self.try_perSlot = int(args[1])

    def choose_arm(self):
        """选择臂"""
        for arm in range(self.n_bandits):
            if self.counts[arm] < self.try_perSlot:
                return arm
        return np.argmax(self.reward)
