# coding=UTF-8
# author: lancezhange

from os.path import join, dirname, abspath, isfile
import ConfigParser
import importlib


class PolicyConfigureHelper(object):
    def __init__(self, n_bandits, conf_filename):
        """
        读取配置文件，初始化 policy

        注意，首个传入参数必须是臂的个数，因此在实验中使用时，先要读取臂的配置获取臂的个数参数
        """
        self.conf_filename = conf_filename
        conf = ConfigParser.ConfigParser()
        configure_path = join(abspath(dirname(__file__)), '..', 'conf', 'policy', self.conf_filename)
        if not isfile(configure_path):
            raise KeyError("configure file " + configure_path + " not exists!")
        conf.read(configure_path)
        if not self.check_conf(conf):
            raise KeyError("configure failed!")
        policy_prototype = class_locate(conf.get("MAB", "policy"))
        if conf.has_option("MAB", "args_policy"):
            self._args_policy = [float(i) for i in conf.get("MAB", "args_policy").split(",")]
            self.policy = policy_prototype([float(n_bandits)] + self._args_policy)
        else:
            self.policy = policy_prototype([float(n_bandits)])  # policy 无参数

    def check_conf(self, conf):
        """
        检查配置
        :param conf:
        :return:
        """
        if not conf.has_section("MAB"):
            print "配置文件 ", self.conf_filename, " 缺失 MAB 段配置！"
            return False
        else:
            if not conf.has_option("MAB", "policy"):
                print "配置文件 ", self.conf_filename, " MAB 段缺失 policy 项!"
                return False
        return True


class BanditConfigureHelper(object):
    def __init__(self, conf_filename):
        """读取配置文件，初始化 bandit"""
        self.conf_filename = conf_filename
        conf = ConfigParser.ConfigParser()
        configure_path = join(abspath(dirname(__file__)), '..', 'conf', 'bandit', self.conf_filename)
        conf.read(configure_path)
        if not self.check_conf(conf):
            print "初始化失败！"
            return
        bandit_prototype = class_locate(conf.get("MAB", "bandit"))
        self._args_bandit = [[float(j) for j in i.split(",")] for i in conf.get("MAB", "args_bandit").split(";")]
        self.bandits = map(lambda (arg): bandit_prototype(arg), self._args_bandit)

    def check_conf(self, conf):
        if not conf.has_section("MAB"):
            print "配置文件 ", self.conf_filename, " 缺失 MAB 段配置！"
            return False
        else:
            if not conf.has_option("MAB", "bandit"):
                print "配置文件 ", self.conf_filename, " MAB 段缺失 bandit 项!"
                return False
        return True


def class_locate(name):
    components = name.rsplit('.', 1)
    module = importlib.import_module(components[0])
    class_name = components[1]
    class_ = getattr(module, class_name)
    return class_
