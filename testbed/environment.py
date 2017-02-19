# coding=UTF-8 
# author: lancezhange


from mabUtils.configureHelper import PolicyConfigureHelper
from mabUtils.configureHelper import BanditConfigureHelper

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


class Environment(object):
    """
    同一环境下比较不同策略的表现
    """

    def __init__(self, bandits_cfg, policies_cfg, label='Multi-Armed Bandit'):
        """
        :type policies_cfg: String
        :type bandits_cfg: String
        """
        bandits_configure = BanditConfigureHelper(bandits_cfg + ".cfg")
        self.bandits = bandits_configure.bandits
        self._n_bandits = len(self.bandits)
        self.policies_cfg = policies_cfg
        self.label = label
        self.policies = [None for _ in range(len(self.policies_cfg))]

    def reset(self):
        self.policies = [PolicyConfigureHelper(self._n_bandits, cfg + ".cfg").policy for cfg in self.policies_cfg]

    def run(self, trials=10, experiments=1):
        scores = np.zeros((trials, len(self.policies)))
        for _ in range(experiments):
            self.reset()
            for t in range(trials):
                for i, policy in enumerate(self.policies):
                    the_choice = policy.choose_arm()
                    reward = self.bandits[the_choice].pull()
                    policy.update(the_choice, reward)
                    scores[t, i] += reward

        return scores / experiments

    def plot_results(self, scores):
        sns.set_style('white')
        sns.set_context('talk')
        plt.title(self.label)
        plt.plot(scores)
        plt.ylabel('Average Reward')
        plt.legend(self.policies_cfg, loc=4)
        plt.xlabel('Pull Count')
        sns.despine()
        plt.show()
