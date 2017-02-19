# coding=UTF-8 
# author: lancezhange


from numpy.random import lognormal
from bandits.bandit import Bandit


class LognormalBandit(Bandit, object):
    """
    对数正态收益
    """
    def __init__(self, args):
        Bandit.__init__(self, args)
        self.mean = self.args[0]
        self.sigma = self.args[1]

    def pull(self):
        """生成本次摇臂收益"""
        return lognormal(self.mean, self.sigma)


x = LognormalBandit([0, 1])
print x.pull()
