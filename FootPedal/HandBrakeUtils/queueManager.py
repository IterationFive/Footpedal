'''
Created on Dec 22, 2022

@author: Cather Steincamp
'''
from FootPedal.lib import CrossThreadList, CrossThreadItem, CrossThreadDict
from FootPedal.config import paths as path
from FootPedal.config import HandBrake as HB
from time import sleep
import re
from shutil import copy2 as filecopy, move as filemove
from os import remove as filedelete, rename as filerename
from FootPedal.HandBrakeUtils import hbProcess
from threading import Thread

''' 
Queue States

    WAITING
        No jobs to convert.  Will convert if jobs are added.
    RUNNING
        Processing, and will continue to process until all items are complete,
        then change to WAITING
    IDLE
        Not currently processing, although there are jobs in the queue.
        Will start again when you tell it.
    IDLEAFTER
        Processing, but after this item is complete, will change
        to IDLE
    STOPAFTER
        Processing, but after this item is complete, will change
        to STOPPED
    STOPPING
        In the process of cancelling a job and cleaning up, then
        will change to STOPPED
    STOPPED
        No longer processing; expecting app shutdown
'''

WAITING, RUNNING, IDLE, IDLEAFTER, STOPAFTER, STOPPING, STOPPED = 0,1,2,3,4,5,6

'''
Item States

    WAITING (variable does double duty)
        No item currently being processed.
        Handbrake CLI is not running.
    CONVERTING
        HandBrakeCLI is currently processing the item.
    SUSPENDED
        HandBrakeCLI has been suspended.
    MOVING
        HandBrakeCLI has completed.
        The file is complete and being moved to its final destination
    BACKINGUP
        HandBrakeCLI has completed.
        The file is being backed up to a second destination
    CLEANUP
        HandBrakeCLI has completed.
        any temporary subtitles being deleted
        original files being moved to trash folder   
        
'''

CONVERTING, SUSPENDED, MOVING, BACKINGUP, CLEANUP = 1,2,3,4,5


class hbQueueManager(object):
    '''
    classdocs
    '''


    def __init__(self, source=path.STAGE, destination=path.OUTPUT, trash=path.TRASH, backup=path.BACKUP,
                 json=HB.JSON, preset=HB.PRESET, guiPreset=HB.GUI_PRESET, params=HB.PARAMS, 
                 log=path.LOG, tmp=path.TMP, cli=HB.CLI, queue=CrossThreadList()):
        '''
        
        All of the following are DEFAULTS, and can be overriden by the individual item
        
            source
                the default location to look for a file (and its subtitles) to convert
            destination
                the default location to put the ouput file when encoding is complete
            trash
                original files (and subtitles) will be moved here when they have been converted
                if None, original files will be left alone
            backup
                a second copy of the file will be made here
                
            json,preset,guiPreset
                default preset configurations
            params
                dictionary.  default CLI parameters

            
        The following CANNOT be overridden 
        
            log
                Where any logs generated by this class will be written.
            cli
                path and filename of Handbrake CLI
            tmp
                where the output file, and temporary subtitle files, will be during conversion
            queue
                CrossThreadList that contains a dictionary of each the items to be processes.
                
        '''
        
        self.source = source 
        self.destination = destination
        self.json = json
        self.guiPreset = guiPreset
        self.preset = preset
        self.params = params 
        self.hb = None
        
        self.tmp = tmp
        self.trash = trash
        self.backup = backup
        self.log = log
        self.queue = queue
        self.cli = cli 
        
        self.runState = CrossThreadItem( WAITING )
        self.jobState = CrossThreadItem( WAITING )
        self.runReport = CrossThreadDict( {'err': 0, 'done':0, 'queued':queue.length(), 'runState': WAITING, 'file':None })
        
        self.process = None
        self.t = Thread( target=self.run)
        self.t.start()
            
        
    def debug(self, debug ):
        f = open ( self.log + 'queueManager.log', 'a' )
        f.write( str( debug ) + '\n' )
        f.close()
        
    def run(self):
        
        while True:
            
            runState = self.runState.get()
            
            if runState == STOPPED:
                break
            elif runState == STOPAFTER or runState == STOPPING:
                # welcome to 'after'
                self.runState.set( STOPPED )
                break
            elif runState == IDLEAFTER:
                # welcome to 'after'
                self.runState.set( IDLE )
                sleep(0.25)
                continue
            elif runState == IDLE:
                sleep(0.25)
                continue
            elif runState == WAITING:
                if self.queue.length() == 0 :
                    sleep( 0.25 )
                else:
                    # what we were waiting for!
                    self.runState.set( RUNNING )
                continue
            elif self.queue.length() == 0 :
                # we're RUNNING But don't need to be anymore
                self.runState.set(WAITING)
                sleep( 0.25 )
                continue
            
            # if we've gotten this far, we are ready to process the next
            # job in queue
            
            job = self.queue.pop(0)
                
            if 'source' in job:
                source = job['source']
            else:
                source = self.source
            if 'source' in job:
                source = job['source']
            else:
                source = self.source
                
            if 'json' in job:
                json = job['json']
            else:
                json = self.json
                
            if 'params' in job:
                params = job['params']
            else:
                params = self.params
                
            if 'preset' in job:
                preset = job['preset']
            else:
                preset = self.preset 
                
            if 'guiPreset' in job:
                guiPreset = job['guiPreset']
            else:
                guiPreset = self.guiPreset
                
                if 'destination' in job:
                    destination = job['destination']
                else:
                    destination = self.destination
                
            if 'srts' in job and len(job['srts']) != 0 :
                    
                srts = []
                
                for i in range( 0, len( job['srts'] ) ):
                    
                    tmpsub = self.tmp + str(i)            
                    
                    r = re.split( '(\....)\.srt$', job['srts'][i] )
                    
                    if len( r ) > 1:
                        tmpsub += r[1]
                        
                    tmpsub += ".srt"
                    
                    filecopy( source + job['srts'][i], tmpsub )
                    srts.append( tmpsub )
                    
            else:
                    
                srts = False
            
            self.process = hbProcess( source + job['file'], self.tmp + job['target'], srts, preset, guiPreset, json, params )
            self.runReport.update( { 'queued': self.queue.length(), 'file': job['target'] })
            self.jobState.set(CONVERTING)
                        
            while self.process.isProcessing():
                
                # really the only thing we need to do here is check and see if the runstate or jobstate has been changed
                # to a state requiring action.  Otherwise we just wait for HandBrake to do its thing.
                
                if self.runState.get() == STOPPING:
                    
                    if self.process.poll() is not None:
                        self.process.murder()
                        sleep(0.25)
                        continue
                    else:
                        break

                jobState = self.jobState.get()
                
                if jobState == SUSPENDED:
                    
                    if self.process.isSuspended()== False:
                        self.process.suspend()
                        
                    sleep(0.25)
                    continue
                
                if jobState == CONVERTING:
                    
                    if self.process.isSuspended():
                        self.process.resume()
                        sleep(0.25)
                        continue
                 
                sleep( 0.25 )
                    
                # end of handbrake process loop
                
            if self.process.data.get( 'success' ) == False:
                
                # the job did not complete successfully.
                
                if self.runState != STOPPING:
                    # looks like handbrake itself failed
                    self.runReport.set( 'err', self.runReport.get('err') + 1 )
                    self.process.writeOutputLog(job['file'])
                    self.jobState.set(CLEANUP)
                    filedelete( self.tmp + job['target'] )
                else:
                    # oh, we MEANT to do that
                    self.runState.set(STOPPED)
                    # we'll break at the beginning of the next loop
                    # but stick around here for cleanup
                    
            else:
                self.runReport.set( 'done', self.runReport.get('done') + 1 )
                
                self.jobState.set( MOVING )
                    
                try:
                    filerename( self.tmp + job['target'], destination + job['target'] )
                except:
                    filemove( self.tmp + job['target'], destination + job['target'] )
                    
                if 'backup' in job:
                    backup = job['backup']
                else:
                    backup = self.backup
                    
                if backup is not None:                        
                    self.jobState.set( BACKINGUP )  
                    filecopy( destination + job['target'], job['backup'] + job['target'] )
                    
                self.jobState.set(CLEANUP)
                    
                if 'trash' in job:
                    trash = job['trash']
                else:
                    trash = self.trash 
                    
                if trash is not None:
                    try:
                        filerename( source + job['file'], trash + job['file'] )
                    except:
                        filemove( source + job['file'], trash + job['file'] )
                              
            # cleanup temporary srts
            
            if srts != False :
                for srt in srts:
                    filedelete(srt)
                    
            # we are now done with the job, one way or another
            
            self.jobState.set(WAITING)
            self.runReport.set( 'file', None )
            self.process = None
            
            # end of main job loop 
        