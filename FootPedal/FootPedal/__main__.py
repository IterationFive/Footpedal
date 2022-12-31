'''
Created on Dec 23, 2022

@author: Cather Steincamp
'''
from lib.CrossThreaders import CrossThreadList
import os 
from HandBrakeUtils import HandbrakeChyron
from HandBrakeUtils import queueManager as qm
from lib.ScreenWrapper import ScreenWrapper
from time import sleep


if __name__ == '__main__':
    pass

    queue = CrossThreadList()
    
    
    files = os.listdir( 'F:/HandCrank/pending/' )
    subfiles = []
    
    for sourcefile in files:
        
        if sourcefile[-3:].lower() == 'srt':
            subfiles.append(sourcefile)
            files.remove(sourcefile)
    
    for sourcefile in files:
        
        if sourcefile[-3:] in ['mkv','mp4','m4v']:
            
            item = { 'file': sourcefile, 'target': sourcefile[:-3] + 'mkv' }
            
            item['subs'] = []
            
            for sub in subfiles:
                
                if sourcefile[:-4] in sub:
                    item['subs'].append( sub )
                    
            if 'Stargirl' in sourcefile:
                item['destination'] = 'D:/Shows/Stargirl/'
                item['backup'] = 'N:/Stargirl/'
            elif 'Prodigy' in sourcefile:
                item['destination'] = 'D:/Shows/Star Trek - Prodigy/'
                item['backup'] = 'N:/Star Trek - Prodigy/'
                
            queue.append(item)
    
    ui = ScreenWrapper( 35, 120 )
    ui.setCursorOn(False)
    ui.setSlot( 'debug', 1,1,20 )
    hbManager = qm.hbQueueManager(queue=queue)
    hbMonitor = HandbrakeChyron( ui, hbManager )
    
    while hbManager.runState.get() != qm.STOPPED:
        sleep(1)
    
    
    