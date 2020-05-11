#!/usr/bin/env python
# -*- coding: utf-8 -*-

class NetworkInformation(object):

    """Network Information Class

    This Class is used to provide a dictionnary with the information of the 
    network according to the different operators.
    """

    def __init__(self):
        self.__dict =  {'ORANGE': None,
                        'SFR': None,
                        'FREE': None,
                        'BOUYGUE': None}
        self.__info = []
        self.__coordonates = []
        self.__distance = {'ORANGE':None,
                           'SFR': None,
                           'FREE': None,
                           'BOUYGUE':None}
    
    # getter 

    def getInfo(self):
        return self.__info
    
    def getCor(self):
        return self.__coordonates
    
    def getDict(self):
        return self.__dict
    
    def getDistance(self):
        return self.__distance 
    
    #setter
    
    def setInfo(self, i):
        self.__info = i
    
    def setCor(self, c):
        self.__coordonates = c
    
    def setDistance(self, op, d):
        self.__distance[op] = d

    def addInfo(self, argument):
        """Dispatch method"""
        method_name = 'op' + str(argument)
        # Get the method from 'self'. Default to a lambda.
        method = getattr(self, method_name, lambda: "Invalid argument")
        # Call the method as we return it
        return method()
 
    def op20801(self): #orange
        self.__dict["ORANGE"] = {'2G':self.getInfo()['2G'],
                                 '3G':self.getInfo()['3G'],
                                 '4G':self.getInfo()['4G']}
 
    def op20810(self): #sfr
        self.__dict["SFR"] = {'2G':self.getInfo()['2G'],
                                '3G':self.getInfo()['3G'],
                                '4G':self.getInfo()['4G']}
 
    def op20815(self): #free
        self.__dict["FREE"] = {'2G':self.getInfo()['2G'],
                               '3G':self.getInfo()['3G'],
                               '4G':self.getInfo()['4G']}
    
    def op20820(self): #bouygue
        self.__dict["BOUYGUE"] = {'2G':self.getInfo()['2G'],
                                  '3G':self.getInfo()['3G'],
                                  '4G':self.getInfo()['4G']}
 