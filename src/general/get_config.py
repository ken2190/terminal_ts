import configparser
import os


def get_config(section, option):
    # 获取当前项目的路径
    pwd = os.getcwd()
    rootDir = os.path.abspath(os.path.dirname(pwd)+os.path.sep+"..")
    # 获取路径到config.ini
    configFilePath = os.path.join(rootDir, 'config.ini')
    # print(configFilePath)
    # 根据section, option 获取配置文件下的值
    conf = configparser.ConfigParser()
    conf.read(configFilePath)
    value = conf.get(section, option)
    return value
