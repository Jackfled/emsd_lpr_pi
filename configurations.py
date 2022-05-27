'''
Read lpr.yaml configurations 
'''

import yaml

class Configurations:
    #  lpr.yaml configurations

    __params = None #yaml.load(open('./lpr.yaml'))

    def __init__(self):
        self.__params = yaml.load(open('./lpr.yaml'))

    def getParam(self, name):
        return self.__params[name]

    def getParams(self):
        return self.__params
     

