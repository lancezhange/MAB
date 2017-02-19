# coding=UTF-8 
# author: lancezhange

import numpy as np
from policies.policy import Policy


class RandomPolicy(Policy, object):
    def __init__(self, args):
        Policy.__init__(self, args)

    def choose_arm(self):
        """选择臂"""
        return np.random.randint(self.n_bandits)
