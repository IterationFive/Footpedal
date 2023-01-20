'''
Created on Dec 22, 2022

@author: Cather Steincamp
'''
from lib import Pwatch
from lib.CrossThreaders import CrossThreadDict
import re 
from time import sleep, time

class hbProcess(Pwatch):
    '''
    This class extends Pwatch for specific use with HandBrake CLI.
    
    information parsed from the output is available through the data 
    attribute, which is a CrossThreadDict.
    
    The following information is available in data.  Items marked
    with an asterisk may return blanks if the most recent output
    does not report that datum.
    
        start:  
            the time() the job was started
        success:
            Whether conversion has completed successfully.  Starts
            as false and is flipped if the right output is seen.
        %
            the percentage as reported by HandBrake
        task*
        taskTotal*
            "Task 1 of 1"
        eta*
            'ETA 00:00:00' or 'Muxing...'
        fpsNow*
        fpsAvg*
            current and average FPS reported by HandBrake
            
    '''


    def __init__(self, sourceFile, outputFile, srts=False, 
                 preset, guiPreset, json, params, cli, log, sublang):
        '''
        sourcefile         
                The full paths and filename of the file to be converted.
        outputfile
                The full path and filename of the output file.
        srts
            list or False, default False
            Any .srt subtitle files to be encoded into the video file.
            Files named whatever.???.srt-- where ??? is an ISO 639-2 language designation
            ( eg. eng, ita, fre, spa, etc. )-- will be encoded with that language specification
            otherwise the language specified in HB.SUB_LANG will be used.            
            
        preset
            A handbrake built-in preset.
            
        guiPreset
            The name of a preset defined in the HandBrake gui, or None.
            
        json
            The full path and filename of a Handbrake JSON config file or None. 
            
        params
            dictionary.  Any parameters to be passed on as arguments to HandBrake
            
        cli
            The full path and filename of the HandbrakeCLI.  
        log
            Folder where logs go.
        '''
        
        self.output = []
        self.data = CrossThreadDict( {'%':''} )
        self.data.set( 'success', False )
        self.log = log
        
        processargs = [ cli ]
        
        if preset != None:
            processargs.extend( ['--preset', preset ] )
            
        if guiPreset != None:
            processargs.extend( ['--preset-import-gui', guiPreset ] )
            
        if json != None:
            processargs.extend( ['--preset-import-file', json ] )
            
        for param in params:
            
            if params[param] == '':
                processargs.extend( param )
            else:
                processargs.extend( [param, params[param] ] )
            
        processargs.extend([ '-i', sourceFile, '-o', outputFile ])
            
        if srts != False :
            
            if type( srts ) == str:
                subs = [ srts ]
            
            sublist = ''
            sublangs = ''
            
            for i in range(0, len(subs)):
                
                sublist += subs[i]
                
                r =  re.split( '\.(...)\.srt$', subs[i] )
                
                if len( r ) > 1 :
                    sublangs += r[1]
                else:
                    sublangs += sublang
                
                if i != len(subs) - 1 :
                    sublist +=','
                    sublangs +=','
                    
            processargs.extend( [ '--srt-file', sublist, '--srt-lang', sublangs ] )
            
        Pwatch.__init__(self, processargs, text=True )
        self.data.set( 'start', time() )
        
    def debug(self, debug):
        f = open( self.log + 'process.log', 'a' )
        f.write( str( debug ) + '\n' )
        f.close()
        
    def processOutput(self, output):
        
        self.output.append( output )
        report={}
        
        r = re.split( 'ask (\d) of (\d)', output )
        
        if len( r ) > 1:
            report['task'] = r[1]
            report['taskTotal'] = r[2]
        else:            
            report['task'] = ''
            report['taskTotal'] = ''
            
        r = re.split( ' (\d{1,2}\.\d\d) \%', output )
        
        if len( r ) > 1:
            report['%'] = r[1] + '%'
        else:
            report['%'] = ''
            
        r = re.split( '\((.*) fps. avg (.*) fps', output )
                
        if len( r ) > 1 :                      
        
            report['fpsNow'] = r[1]
            report['fpsAvg'] = r[2]
        else:
            report['fpsNow'] = ''
            report['fpsAvg'] = ''
                    
        r = re.split( 'ETA (..)h(..)m(..)s', output )
        
        if len( r ) > 1 :
            report['eta'] = 'ETA ' + r[1] + ':' + r[2] + ':' + r[3]
        elif len( re.split( '(mux\: track|Muxing \:)', output ) ) > 1:
            report['eta'] = '   Muxing...'
        else:
            report['eta'] = ''
                
        if len( re.split( 'Encode done\!|Finished work', output ) ) > 1:
            report['success'] = True
            
        self.data.update(report)
        sleep(0.05)
        
    def writeOutputLog(self, filename):
        f = open( self.log + filename + '.log', 'w' )
        for line in self.output:
            f.write( line + '\n' )
        f.close()
        
        
        
        
        