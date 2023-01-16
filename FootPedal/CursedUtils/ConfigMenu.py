'''
Created on Jan 14, 2023

@author: Cather Steincamp
'''

import CursedUtils as cu

CONFIGFILE = './footpedal.config'

class ConfigMenu(cu.Window):
    '''
    classdocs
    '''

    def __init__(self, parent, menuData:dict,):
        self.menuData = menuData
        cu.Window.__init__(self, parent, 25, 110, 1, 5)
        
    def fillFields(self):
        pass
        
        