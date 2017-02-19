# -* - coding: UTF-8 -* -

from mabUtils.configureHelper import PolicyConfigureHelper
from mabUtils.configureHelper import BanditConfigureHelper

banditConfigure = BanditConfigureHelper("bernoulli.cfg")
bandits = banditConfigure.bandits

n_bandits = len(bandits)

policyConfigure = PolicyConfigureHelper(n_bandits, "epsilon_greedy.cfg")
policy = policyConfigure.policy

exp_number = 1000

# 实验
for i in xrange(exp_number):
    the_choice = policy.choose_arm()
    reward = bandits[the_choice].pull()
    policy.update(the_choice, reward)

# 打印实验结果
policy.print_result()

