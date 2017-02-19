# coding=UTF-8 
# author: lancezhange


import numpy as np
from policies.policy import Policy
import math


class EXP4Policy(Policy, object):
    """
    Exponential weighting for Exploration and Exploitation with Experts.

    """

    def __init__(self, args):
        Policy.__init__(self, args)

    def choose_arm(self):
        raise NotImplemented

    def update(self, arm, reward):
        raise NotImplemented
