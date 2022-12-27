'''
Created on Dec 22, 2022

@author: Cather Steincamp
'''

import HandBrakeUtils.queueManager as qm
from CursedUtils import ScreenHandler
from time import sleep
from threading import Thread

class HandbrakeChyron(object):
    '''
    classdocs
    '''


    def __init__(self, window:ScreenHandler, hqm:qm.hbQueueManager):
        '''
        Constructor
        '''
        self.window = window
        self.hqm = hqm
        
        
        y = window.sizeY - 4
        maxX = window.sizeX - 2
        
        window.setSlot( 'hbTitleBar', y, 1, maxX )
        window.setSlot( 'hbJobStatus', y + 1, 1, maxX - 42 )
        window.setSlot( 'hbJobETA', y + 1, maxX - 19, 12 )
        window.setSlot( 'hbJob%', y + 1 , maxX - 6, 6 )
        window.setSlot( 'hbQueueStatus', y + 2, 1, maxX - 19 )
        window.setSlot( 'hbJobFPS', y + 2, maxX - 17 , 17 )
        window.refresh()
        window.nap( 3500 )
        
        self.t = Thread( target = self.display )
        self.t.start()
        
    def debug(self, debug):
        f= open( '../../hqm.log', 'a')
        f.write( str( debug ) + '\n')
        f.close()
        
    def display(self):
        
        while True:
            
            runState = self.hqm.runState.get()
            runReport = self.hqm.runReport.d
            bragstring = str( runReport['done'] ) + ' file(s) completed, ' + str( runReport['err'] ) + ' failed, ' + str( runReport['queued'] ) + ' queued'
            
            if runState == qm.WAITING:
                                
                self.window.slotWriteNow( 'hbTitleBar', 'No Files Queued' )
                self.window.slotWriteNow( 'hbJobStatus', 'Processing Idle' )
                self.window.slotWriteNow( 'hbJobETA', '' )
                self.window.slotWriteNow( 'hbJob%', '' )
                self.window.slotWriteNow( 'hbQueueStatus', bragstring ) 
                self.window.slotWriteNow( 'hbJobFPS', '' )
                sleep(0.1)
                
                
                continue
            
            if runState == qm.IDLE:
                self.window.slotWriteNow( 'hbTitleBar', 'Processing Idle' )
                self.window.slotWriteNow( 'hbJobStatus', '' )
                self.window.slotWriteNow( 'hbJobETA', '' )
                self.window.slotWriteNow( 'hbJob%', '' )
                self.window.slotWriteNow( 'hbQueueStatus', bragstring ) 
                self.window.slotWriteNow( 'hbJobFPS', '' )
                sleep(0.1)
                continue
            
            if runState == qm.STOPPING:
                self.window.slotWriteNow( 'hbTitleBar', 'Shutting down...' )
                self.window.slotWriteNow( 'hbJobStatus', '' )
                self.window.slotWriteNow( 'hbJobETA', '' )
                self.window.slotWriteNow( 'hbJob%', '' )
                self.window.slotWriteNow( 'hbQueueStatus', bragstring ) 
                self.window.slotWriteNow( 'hbJobFPS', '' )
                sleep(0.1)
                continue
            
            if runState == qm.STOPPED:
                break
            
            # all remaining states involve a currently processing job
            
            self.window.slotWriteNow( 'hbTitleBar', runReport['file'] )
            
            if runState == qm.IDLEAFTER:
                self.window.slotWriteNow( 'hbQueueStatus', bragstring + ' (Going Idle after this file)' )
            elif runState == qm.STOPAFTER:
                self.window.slotWriteNow( 'hbQueueStatus', bragstring + ' (Shutting down after this file)')
            else:
                self.window.slotWriteNow( 'hbQueueStatus', bragstring )
                
            jobState = self.hqm.jobState.get()
            
            if jobState == qm.CONVERTING:                
                jobInfo = self.hqm.process.data.copy()
                #TODO Elapsed Time
                
                if jobInfo['%'] == '':
                    # this is one of the fields that doesn't blank out
                    # so if it's not set, then we're just starting up
                    self.window.slotWriteNow( 'hbJobStatus', 'Starting up...' )
                    self.window.slotWriteNow( 'hbJobETA', '' )
                    self.window.slotWriteNow( 'hbJob%', '' )
                    self.window.slotWriteNow( 'hbQueueStatus', bragstring ) 
                    self.window.slotWriteNow( 'hbJobFPS', '' )
                    
                else:
                    
                    if jobInfo['fpsNow'] != '' and jobInfo['fpsNow'][0:2] != '00':                     
                        self.window.slotWriteNow( 'hbJobFPS', jobInfo['fpsNow'] + 'fps/' + jobInfo['fpsAvg'] +'avg' )
                        
                    if jobInfo['task'] != '' and jobInfo['taskTotal'] != '':
                        self.window.slotWriteNow( 'hbJobStatus', 'Converting, task ' + jobInfo['task'] + ' of ' + jobInfo['taskTotal'] )
                    else:
                        self.window.slotWriteNow( 'hbJobStatus', 'Converting')
                        
                    if jobInfo['eta'] != '':
                        self.window.slotWriteNow( 'hbJobETA', jobInfo['eta'] )
                                                  
                    if len( jobInfo['%'] ) == 5 :
                        jobInfo['%'] = '0' + jobInfo['%']
                        
                    self.window.slotWriteNow('hbJob%', jobInfo['%'])
                        
            elif jobState == qm.SUSPENDED:
                jobInfo = self.hqm.hbProcess.data.copy()
                self.window.slotWriteNow( 'hbJobStatus', 'Processing Suspended' )
                self.window.slotWriteNow( 'hbJobETA', '' )
                self.window.slotWriteNow( 'hbQueueStatus', '1 file suspended, ' + bragstring ) 
                self.window.slotWriteNow( 'hbJobFPS', '' )
                
                if jobInfo['%'] != '':                
                    if len( jobInfo['%'] ) == 4:
                        jobInfo['%'] = '0' + jobInfo['%']
                    self.window.slotWriteNow('hbJob%', jobInfo['%'])
                    
            else:
                    
                if jobState == qm.MOVING:
                    self.window.slotWriteNow( 'hbJobStatus', 'Moving file to destination' )
                        
                elif jobState == qm.BACKINGUP:
                    self.window.slotWriteNow( 'hbJobStatus', 'Creating Backup' )
                        
                elif jobState == qm.CLEANUP:
                    self.window.slotWriteNow( 'hbJobStatus', 'Cleaning up' )


                self.window.slotWriteNow( 'hbJobETA', '' )
                self.window.slotWriteNow( 'hbJob%', '' )
                self.window.slotWriteNow( 'hbQueueStatus', bragstring ) 
                self.window.slotWriteNow( 'hbJobFPS', '' )
                    
            sleep( 0.125 )
                    
            
            
                
                
            
            
            