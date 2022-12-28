'''
Created on Dec 27, 2022

@author: Cather Steincamp
'''

from CursedUtils.keymaps import KEYMAP

class KeyResponses(object):
    '''
    Creates a set of responses to keys.  
    '''


    def __init__(self, activateKeypad=True, translateNumpad=True, caseSensitive=False):
        '''
            activateKeypad
                determines if the keystroke handler will set window.keypad( True )
            translateNumpad
                determines if the numpad version of the keys will be treated the
                same as their counterparts
            caseSensitive
                determines if uppercase letters are treated as different input that their lowercase
                counterparts
                If true, all uppercase characters will be translated to lowercase when assigned,
                and the keyProcessor 
        '''
        self.activateKeypad=activateKeypad
        self.translateNumpad=translateNumpad
        self.caseSensitive=caseSensitive
        
        self.responses = {}
        self.aliases = {}
        
    def setResponse(self, key, action, passKeystroke=False, passKeyNumber=False, args=None, kwargs=None):
        '''
            key
                the number, character, or special string corresponding to the keystroke 
                to which we want to respond
            action
                the function (passed as reference!) to run when they key is pressed
                
            passKeystroke
                if True, will pass the character or special string to the action
                as the first parameter
                
                if a string, will pass it as a keyword argument, using the 
                string as the keyword
                
            passKeyNumber
                if True, will pass the number corresponding to the keystroke as 
                the first parameter (or second, if for some reason you're using
                passKeystroke as well)
                
                if a string, will pass it as a keyword argument, using the 
                string as the keyword
                
                
            args 
                list or None
                Any arguments here will be passed to the action in the order
                provided.  If passKeystroke or PassKeynumber is True,
                then these arguments will come after those.
            kwargs
                dict or None
                This dictionary (if present) will be passed to the action
                as keyword arguments.
                
                IMPORTANT NOTE: any kwargs in this dictionary can be overwritten
                by the kwargs provided by passKeystroke, passKeyNumber, or
                the keystroke Handler itself.
                
                            
        '''
        
        key = self.translateKey(key)
                
        if key != False:
            
            if self.caseSensitive == False and key > 64 and key < 91 : #65-90 is A-Z
                key += 32 
            
            response = { 'action': action  }
            if passKeystroke != False:
                response['passKeystroke'] = passKeystroke
            if passKeyNumber != False:
                response['passKeyNumber'] = passKeyNumber
            if args is not None:
                response['args'] = args
            if kwargs is not None:
                response['kwargs'] = kwargs
                
            self.responses[key] = response
            
    def translateKey(self, key ):
        
        if type( key ) == str:
            if len( key ) == 1:
                #just a keystroke
                key = ord( key )
            elif key in KEYMAP:
                #non-character key
                key = KEYMAP[key]
                
        if type( key ) == int:
            return key
        else:
            return False
            
    def clearResponse(self, key):        
        if key in self.responses:
            del self.responses[key]
            
    def setAlias(self, pressThisKey, butReportThisKey ):
        pressThisKey = self.translateKey(pressThisKey)
        butReportThisKey = self.translateKey(butReportThisKey)
        
        if pressThisKey != False and butReportThisKey != False:
            self.aliases[pressThisKey] = butReportThisKey
            
    def copy(self):
        
        r = KeyResponses( self.activateKeypad, self.translateNumpad, self.caseSenstive )
        r.aliases = self.aliases.copy()
        
        for key in self.responses:
            r.setResponse(key, **self.responses[key])
            
        return r
        