'''
Created on Jan 18, 2023

@author: Cather Steincamp
'''

from FootPedal import MAINCONFIG, SHOWCONFIG, LOGDIR, QUEUEFILE
import CursedUtils as cu
from HandBrakeUtils.queueManager import hbQueueManager, STOPPING
from lib import CrossThreadDict
import FootPedal.menus as menu
from _ast import arg

class MainMenu(object):
    '''
    classdocs
    '''


    def __init__(self, window:cu.Screen, qm:hbQueueManager, config:CrossThreadDict ):
        '''
        Constructor
        '''
        self.window = window
        self.qm = qm
        self.fileQueue = qm.queue
        self.config = config
        
        midpoint = int( window.sizeX / 2 )
        
        self.window.setSlot('title',1, midpoint - 20, 40, cu.CENTER )
        self.window.slotWrite( 'title', 'FootPedal Main Menu' )
        
        leftKeyX = midpoint - 27
        leftLabelX = midpoint - 25
        rightKeyX = midpoint + 2
        rightLabelX = midpoint + 4
        
        self.window.write( 4, leftKeyX, 'H' )
        self.window.write( 4, leftLabelX, 'Handbrake Configuration' )
        self.window.write( 4, rightKeyX, 'F' )
        self.window.write( 4, rightLabelX, 'Folder Configuration' )
        
        self.window.write( 6, leftKeyX, 'T' )
        self.window.write( 6, leftLabelX, 'TV Show Presets' )
        self.window.write( 6, rightKeyX, 'Q' )
        self.window.write( 6, rightLabelX, 'Queue Management' )
        
        self.window.write( 8, leftKeyX, 'S' )
        self.window.write( 8, leftLabelX, 'Scan Inbox' )
        self.window.write( 8, rightKeyX, 'P' )
        self.window.write( 8, rightLabelX, 'Pause Processing' )
        
        self.window.write( 10, leftLabelX, 'Press Esc to Cancel Processing and Exit' )
        
        self.window.refresh()
        
        self.keys = cu.KeyResponder()
        self.keys.setResponse('h', self.openHandBrakeConfig)
        self.keys.setResponse('f', self.openFolderConfig)
        self.keys.setResponse('escape', qm.runState.set, args=[STOPPING] )
        
        self.keys.keyLoop(window)
        
        
        
        
        
    def openHandBrakeConfig(self):
        
        x = menu.HandbrakeConfig(self.window)
        x.runMenu()
        x.close()
        
    def openFolderConfig(self):
        
        x = menu.PathConfig(self.window)
        x.runMenu()
        x.close()
        