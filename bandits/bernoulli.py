# coding=utf-8
# author: lancezhange

import random
from bandits.bandit import Bandit


class BernoulliBandit(Bandit, object):
    """
    伯努利收益臂（其实单次是两点分布）
    给定概率p， 以概率p获得收益1，1-p获得收益0
    """
    def __init__(self, args):
        Bandit.__init__(self, args)
        # 成功概率
        self.p = self.args[0]

    def pull(self):
        """生成本次摇臂收益"""
        if random.random() > self.p:
            return 0.0
        else:
            return 1.0

if __name__ == '__main__':
    x = BernoulliBandit([0.5])
    print x.pull()
