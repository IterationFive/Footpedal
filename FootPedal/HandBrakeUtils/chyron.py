'''
Created on Dec 22, 2022

@author: Cather Steincamp
'''

import HandBrakeUtils.queueManager as qm
from CursedUtils import Screen
from time import sleep
from threading import Thread

class HandbrakeChyron(object):
    '''
    classdocs
    '''


    def __init__(self, window:Screen, hqm:qm.hbQueueManager):
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
            runReport = self.hqm.runReport.copy()
            bragstring = str( runReport['done'] ) + ' file(s) completed, ' + str( runReport['err'] ) + ' failed, ' + str( runReport['queued'] ) + ' queued'
            
            if runState == qm.WAITING:
                                
                self.window.slotWrite( 'hbTitleBar', 'No Files Queued' )
                self.window.slotWrite( 'hbJobStatus', 'Processing Idle' )
                self.window.slotWrite( 'hbJobETA', '' )
                self.window.slotWrite( 'hbJob%', '' )
                self.window.slotWrite( 'hbQueueStatus', bragstring ) 
                self.window.slotWrite( 'hbJobFPS', '' )
                self.window.refresh()
                sleep(0.1)
                
                
                continue
            
            if runState == qm.IDLE:
                self.window.slotWrite( 'hbTitleBar', 'Processing Idle' )
                self.window.slotWrite( 'hbJobStatus', '' )
                self.window.slotWrite( 'hbJobETA', '' )
                self.window.slotWrite( 'hbJob%', '' )
                self.window.slotWrite( 'hbQueueStatus', bragstring ) 
                self.window.slotWrite( 'hbJobFPS', '' )
                self.window.refresh()
                sleep(0.1)
                continue
            
            if runState == qm.STOPPING:
                self.window.slotWrite( 'hbTitleBar', 'Shutting down...' )
                self.window.slotWrite( 'hbJobStatus', '' )
                self.window.slotWrite( 'hbJobETA', '' )
                self.window.slotWrite( 'hbJob%', '' )
                self.window.slotWrite( 'hbQueueStatus', bragstring ) 
                self.window.slotWrite( 'hbJobFPS', '' )
                self.window.refresh()
                sleep(0.1)
                continue
            
            if runState == qm.STOPPED:
                break
            
            # all remaining states involve a currently processing job
            
            self.window.slotWrite( 'hbTitleBar', runReport['file'] )
            
            if runState == qm.IDLEAFTER:
                self.window.slotWrite( 'hbQueueStatus', bragstring + ' (Going Idle after this file)' )
                self.window.refresh()
            elif runState == qm.STOPAFTER:
                self.window.slotWrite( 'hbQueueStatus', bragstring + ' (Shutting down after this file)')
                self.window.refresh()
            else:
                self.window.slotWrite( 'hbQueueStatus', bragstring )
                self.window.refresh()
                
            jobState = self.hqm.jobState.get()
            
            if jobState == qm.CONVERTING:                
                jobInfo = self.hqm.process.data.copy()
                #TODO Elapsed Time
                
                if jobInfo['%'] == '':
                    # this is one of the fields that doesn't blank out
                    # so if it's not set, then we're just starting up
                    self.window.slotWrite( 'hbJobStatus', 'Starting up...' )
                    self.window.slotWrite( 'hbJobETA', '' )
                    self.window.slotWrite( 'hbJob%', '' )
                    self.window.slotWrite( 'hbQueueStatus', bragstring ) 
                    self.window.slotWrite( 'hbJobFPS', '' )
                    self.window.refresh()
                    
                else:
                    
                    if jobInfo['fpsNow'] != '' and jobInfo['fpsNow'][0:2] != '00':                     
                        self.window.slotWrite( 'hbJobFPS', jobInfo['fpsNow'] + 'fps/' + jobInfo['fpsAvg'] +'avg' )
                        self.window.refresh()
                        
                    if jobInfo['task'] != '' and jobInfo['taskTotal'] != '':
                        self.window.slotWrite( 'hbJobStatus', 'Converting, task ' + jobInfo['task'] + ' of ' + jobInfo['taskTotal'] )
                        self.window.refresh()
                    else:
                        self.window.slotWrite( 'hbJobStatus', 'Converting')
                        self.window.refresh()
                        
                    if jobInfo['eta'] != '':
                        self.window.slotWrite( 'hbJobETA', jobInfo['eta'] )
                        self.window.refresh()
                                                  
                    if len( jobInfo['%'] ) == 5 :
                        jobInfo['%'] = '0' + jobInfo['%']
                        
                    self.window.slotWrite('hbJob%', jobInfo['%'])
                    self.window.refresh()
                        
            elif jobState == qm.SUSPENDED:
                jobInfo = self.hqm.hbProcess.data.copy()
                self.window.slotWrite( 'hbJobStatus', 'Processing Suspended' )
                self.window.slotWrite( 'hbJobETA', '' )
                self.window.slotWrite( 'hbQueueStatus', '1 file suspended, ' + bragstring ) 
                self.window.slotWrite( 'hbJobFPS', '' )
                
                if jobInfo['%'] != '':                
                    if len( jobInfo['%'] ) == 4:
                        jobInfo['%'] = '0' + jobInfo['%']
                    self.window.slotWrite('hbJob%', jobInfo['%'])
                self.window.refresh()
                    
            else:
                    
                if jobState == qm.MOVING:
                    self.window.slotWrite( 'hbJobStatus', 'Moving file to destination' )
                    self.window.refresh()
                        
                elif jobState == qm.BACKINGUP:
                    self.window.slotWrite( 'hbJobStatus', 'Creating Backup' )
                    self.window.refresh()
                        
                elif jobState == qm.CLEANUP:
                    self.window.slotWrite( 'hbJobStatus', 'Cleaning up' )
                    self.window.refresh()


                self.window.slotWrite( 'hbJobETA', '' )
                self.window.slotWrite( 'hbJob%', '' )
                self.window.slotWrite( 'hbQueueStatus', bragstring ) 
                self.window.slotWrite( 'hbJobFPS', '' )
                self.window.refresh()
                    
            sleep( 0.125 )
                    
            
            
                
                
            
            
            