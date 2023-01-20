'''
Created on Jan 17, 2023

@author: Cather Steincamp
'''
    
import CursedUtils as cu
import os, json
from FootPedal.menus.PathConfig import PathConfig
from FootPedal.menus.HandbrakeConfig import HandbrakeConfig
from FootPedal.menus.MainMenu import MainMenu
from lib.CrossThreaders import CrossThreadList
from HandBrakeUtils.queueManager import hbQueueManager
from HandBrakeUtils.chyron import HandbrakeChyron

from FootPedal import MAINCONFIG, SHOWCONFIG, LOGDIR, QUEUEFILE

if __name__ == '__main__':

    if os.path.isfile( MAINCONFIG ):
        f = open( MAINCONFIG, 'r' )
        config = json.load( f )
        f.close()
    else:
        config = {} 
    
    ui = cu.Screen(30, 120)

    if 'paths' not in config:
        m = PathConfig( ui )
        m.firstRun()
        config = m.config
        m.close()

    if 'handbrake' not in config:
        m = HandbrakeConfig( ui )
        m.firstRun()
        config = m.config
        m.close()
    
    if os.path.isfile( QUEUEFILE ):
        f = open( QUEUEFILE, 'r' )
        fileQueue = CrossThreadList( json.load( f ) ) 
        f.close()
    else:
        fileQueue = CrossThreadList()
        
    qm = hbQueueManager(source=config['paths']['Staging'], destination=config['paths']['Outbox'], trash=config['paths']['Trash'], 
                        backup=config['paths']['Backup'], json=config['handbrake']['JSON Config'],  
                        preset=config['handbrake']['Preset'], guiPreset=config['handbrake']['GUI Preset'], params={}, 
                        tmp=config['paths']['Temp'], cli=config['handbrake']['Handbrake CLI'], 
                        sublang=config['handbrake']['Subtitle Language'], log=LOGDIR, queue=fileQueue)
    
    chyron = HandbrakeChyron(ui, qm)
    
    main = MainMenu( ui, qm, chyron, fileQueue )
    
    ui.close()