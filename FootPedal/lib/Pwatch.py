'''
Created on Dec 10, 2022

@author: Cather Steincamp

    Pwatch extends Popen, and has all of the same arguments excepting STDOUT, 
    which is set to PIPE.  The default value for stderr has been changed to
    STDOUT.  
    
    IMPORTANT:  For reasons I have yet to ascertain, if 'stderr' is set to PIPE, 
    the process locks when used for what I'm using it for.  I've left the code 
    in place because damnit, it should work.
    
    NonitoredProcess adds the following properties.
    
        errHandling       tracks if output has its own pipe
        processing        tracks if output processing has completed
        suspended         tracks if the process has been suspended
        
        runlock            threading.Lock()        
        process            a psutil Process() object for suspending and resuming the process
        
        tOut               a thread for processOutput()
        tErr (optional)    a thread for processError()
        
    NonitoredProcess adds the following methods:
    
        suspend()
        resume()    
                    what it says on the tin
        
        isProcessing()    
                    returns boolean
                    This means "has it finished processing the data", not whether the 
                    process itself has finished or has been terminated or suspended
                    
                    Use this instead of poll() to make sure you're waiting until 
                    all data has processed.
                    
        isSuspended()
                    returns boolean
                    speaks only to the suspended state, not whether the process
                    has completed.  A completed process will not register
                    as suspended.  
                    
        errorMonitor()
                    runs in its own thread.  Processes output from STDERR and passes
                    each line to processError().  Only executed if stderr is set to PIPE.
                    
                    Stops running when the process ends.
                    
        outputMonitor()
                    runs in its own thread.  Processes output from STDOUT and passes
                    each line to processOutput().
                    
                    When the process ends, will process any remaining STDOUT output
                    using processOutput(), as well as (if stderr is set to PIPE) anything 
                    remaining from STDERR using processError()
        
        processOutput( output)
        processError( error )
                    As mentioned above, these methods are called from outputMonitor() and
                    are used to process each line of STDOUT or STDERR.  In this class, 
                    they are empty, as they are there for the use of child classes.
'''

from subprocess import Popen, PIPE, STDOUT
from threading import Thread, Lock
from psutil import Process

class Pwatch(Popen):
    
    def __init__(self, args, stderr=STDOUT, **kwargs):
        
        if 'stdout' in kwargs:
            del kwargs['stdout']           
                
        self.errHandling = stderr
        self.processing = True
        self.suspended = False
        self.runlock = Lock()
        
        Popen.__init__(self, args, stdout=PIPE, stderr=stderr, **kwargs )
        
        self.process = Process( self.pid )
        
        self.tOut = Thread( target = self.outputMonitor )
        self.tOut.start()
        
        if stderr == PIPE:
            self.tErr = Thread( target = self.errorMonitor )
            self.tErr.start()
        
    def suspend(self):
        with self.runlock:
            if self.suspended == False:
                self.process.suspend()
                self.suspended = True 
             
    def resume(self):
        with self.runlock:
            if self.suspended:
                self.process.resume()
                self.suspended = False 
                
    def murder(self):
        # for those days when terminate() and kill() 
        # aren't getting the job done
        self.process.kill()
    
    def isProcessing(self):
        with self.runlock:
            return self.processing
        
    def isSuspended(self):
        with self.runlock:
            return self.suspended    
            
    def outputMonitor(self):        
                    
        while self.poll() is None:
            output = self.stdout.readline().rstrip()                         
            if  len( output ) > 0 :
                self.processOutput( output )
                    
        # process is done, get the last of it
    
        output, error = self.communicate()
        
        for line in output.split( '\n' ):
            self.processOutput( line )
        
        if self.errHandling == PIPE:
            self.tErr.join()
            for line in error.split( '\n' ):
                self.processError( line )
        
        with self.runlock:
            self.processing = False 
                    
    def errorMonitor(self):
           
        while self.poll() is None: 
            error = self.stderr.readline().rstrip()
            if  len( error ) > 0 :
                self.processError( error )
                               
    def processOutput(self, output ):
        pass            
    def processError(self, error ):
        pass                       