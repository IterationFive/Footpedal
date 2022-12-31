'''
Created on Dec 27, 2022

@author: Cather Steincamp
'''

import curses
import os, json

mapdir = 'B:/FootPedal/FootPedal/CursedUtils/keymaps/'




class keyMapper(object):
    
    def __init__(self, mapdir, maplabel ):
        self.maplabel = maplabel
        self.mapdir = mapdir
        self.loadmap()
        self.stdscr = curses.initscr()
        self.stdscr.keypad( True )
        
        self.write( 'Press Escape' )
        
        self.map['escape'] = self.stdscr.getch()
                
        self.write( 'Press Backspace' )
        
        backspace = self.stdscr.getch()
        
        self.map['backspace'] = backspace
        
        # we had to do those manually because they are used to reject
        # and correct
        
        # now let's build and process the list
        
        c = 'ctrl+'
        a = 'alt+'
        s = 'shift+'
        
        keys = []
        
        for mod in [c,a,s]:
            for key in [ 'backspace', 'escape' ]:
                keys.append( mod+key )
        for mod in ['', c,a,s]:
            for i in range( 1, 13) :
                keys.append( mod+'f' + str(i) )
        for mod in [c,a]:
            for i in range(ord('a'),ord('z')+1):
                keys.append( mod+chr(i) )
        for mod in ['', c,a,s]:
            for spec in ['','pad'] :
                for key in ['tab', 'enter','insert','delete','home','end','pageup','pagedown','up','down','left','right']:
                    keys.append( mod+spec+key )
        for mod in ['', c,s,a]: # there is no non-pad version of padcenter
            keys.append( mod+'padcenter' )
        
        for mod in [c,a]:
            for key in [ '1','2','3','4','5','6','7','8','9','0','`','-','=','[',']','\\',':',"'",',','.','/']:
                keys.append( mod+key )
        
        
                
        i = 0
        
        while i < len( keys ):
            
            if keys[i] in self.map or keys[i] in self.unavailable or keys[i] in self.dead or keys[i] in self.duplicates:
                i +=1 
                continue
            
            i += self.testKey( keys[i] )
            
        curses.endwin()
        
        print( self.map)
        
        '''
            Escape & variations, Backspace, Enter and Variations, Padenter & Variations
            
            (manual choice, remember backspace and escape)
            
            build list
                
                f1 keys & variations
                
                alt & ctrl variations of letters, numbers, and `-=[]\;',./\
                
                nav keys & variations
                
                pad keys & variations
            
            cycle through list, SKIPPING ANYTHING ALREADY DEFINED
            
                if esc, mark as unusable
                if backspace, go back one
                
                compare to existing list, note duplicates
                leave duplicates in the map
        
        '''   
    def testKey(self, label):
        
        self.write( label )
        
        x = self.stdscr.getch()
        
        if x == self.map[ 'escape'] :
            self.unavailable.append( label )
            self.saveemap()
            return 1
        elif x == self.map['backspace']:
            return -1
        elif x == 0:
            self.dead.append(label)
            self.saveemap()
            return 1
        elif x != 127 and x > 65 and x < 256:
            # ignore. you probably pasted.
            return 0
        else:            
            # check to see if it is a duplicate
            
            new = True
            
            for key in self.map:
                
                if x == self.map[key] and key != label:
                    new = False
                    self.duplicates[label] = key
                    self.saveemap()
                    break 
            
            if new:
                self.map[label] = x 
                self.saveemap()
            return 1
        
        
        
        
        
        
        
        
        
        
        
        
        
    def write(self, message ):
        self.stdscr.addstr( 10, 10, message + '                             ' )
        self.stdscr.refresh()
            
    def saveemap(self):        
        f = open( self.mapdir + self.maplabel + '.map.json', 'w' )
        json.dump( self.map, f )
        f.close()
        f = open( self.mapdir + self.maplabel + '.duplicate.json', 'w' )
        json.dump( self.duplicates, f )
        f.close()
        f = open( self.mapdir + self.maplabel + '.unavailable.json', 'w' )
        json.dump( self.unavailable, f )
        f.close()
        f = open( self.mapdir + self.maplabel + '.dead.json', 'w' )
        json.dump( self.dead, f )
        f.close()
        
          
            
    def loadmap(self):        
        if os.path.exists( self.mapdir + self.maplabel + '.map.json' ):
            f = open( self.mapdir + self.maplabel + '.map.json' )
            self.map = json.load( f )
            f.close()
        else:
            self.map = {}
            
        if os.path.exists( self.mapdir + self.maplabel + '.duplicate.json' ):
            f = open( self.mapdir + self.maplabel + '.duplicate.json', 'r' )
            self.duplicates = json.load( f )
            f.close()
        else:
            self.duplicates = {}
            
        if os.path.exists( self.mapdir + self.maplabel + '.unavailable.json' ):
            f = open( self.mapdir + self.maplabel + '.unavailable.json', 'r' )
            self.unavailable = json.load( f )
            f.close()
        else:
            self.unavailable = []
            
        if os.path.exists( self.mapdir + self.maplabel + '.dead.json' ):
            f = open( self.mapdir + self.maplabel + '.dead.json', 'r' )
            self.dead = json.load( f )
            f.close()
        else:
            self.dead = []

a = keyMapper( mapdir, 'test' )
