'''
Created on Dec 27, 2022

@author: Cather Steincamp
'''

from CursedUtils.keymaps import KEYMAP, PADTRANSLATOR

class KeyResponder(object):
    '''
    This class is defined to simplify the use of keys in curses.
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
        self.disabled = {}
        
    def setResponse(self, key, action, passKeystroke=False, passKeyNumber=False, args=None, kwargs=None):
        '''
            key
                the number, character, or special string corresponding to the keystroke 
                to which we want to respond, or 'default'
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
            
    def clearResponse(self, key):        
        if key in self.responses:
            del self.responses[key]
            
    def translateKey(self, key ):
        # converts a character or map string to 
        # the corresponding number
        
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
            
    def setAlias(self, pressThisKey, butReportThisKey ):
        '''
            allows you to set a key to respond as if it were another key
            it passKey or passNumber is set in the response, it will pass
            the SECOND key, not the key you pressed.
        '''
        pressThisKey = self.translateKey(pressThisKey)
        butReportThisKey = self.translateKey(butReportThisKey)
        
        if pressThisKey != False and butReportThisKey != False:
            self.aliases[pressThisKey] = butReportThisKey
            
    def copy(self):
        '''
            produces a "deep" copy of the object instance
        '''
        
        r = KeyResponder( self.activateKeypad, self.translateNumpad, self.caseSenstive )
        r.aliases = self.aliases.copy()
        
        for key in self.responses:
            r.setResponse(key, **self.responses[key])
            
        return r
    
    def merge(self, responder):
        '''
            incorporates the aliases and responses from another
            keyResponder object; the aliases and responses
            from the imported object will have priority
        '''
        
        self.aliases.update( responder.aliases )
        self.responses.update( responder.responses )
        self.disabled.update( responder.disabled )
    
    def reverseLookup(self, keyNumber):
        # produces character or mapstring from number
        
        for i in KEYMAP:
            if keyNumber == KEYMAP[i]:
                return i
            
        return( chr( keyNumber ))
            
    def respond(self, key, *moreargs, **morekwargs):
        '''
            takes the number provided by window.getch() and, 
            checks to see if it needs to be:
                converted to lowercase (if self.caseSensitive is False)
                converted to an alias 
                converted from a numpad key to its non-numpad counter part (if self.translateNumpad is True)
                
            If the key has a response assigned, or if there is a 'default' assignment,
            then the action assigned will be executed, with any arguments provided in the response
            definition, as well as any additional arguments provided as moreargs and morekwargs.
            
            the order of positional arguments is:
                provided by passKey (if set in response)
                provided by PassNumber (if set in response)
                specified in response['args']
                specified here
                
            The order of priority for keyword arguments is:
                passKey and/or passNumber, if set in response, override all
                arguments provided here will override arguments in repsonse['kwargs']
                response['kwargs'] overrides nothing
                
            returns -1 if no response is defined
        '''
        
        if self.caseSensitive == False and key > 64 and key < 91: #A-Z are 65-90
            key += 32 #a-z are 97 to 122
        
        if key in self.aliases:
            key = self.aliases[ key ]
                
        if self.translateNumpad and key in PADTRANSLATOR:
            key = PADTRANSLATOR[ key ]
        
        if key in self.responses:
            response =  self.responses[key]
        elif 'default' in self.responses:
            response =  self.responses['default']
        else:
            response = False
            
        if response != False:
            
            if 'args' in response:
                args = response['args'].extend( moreargs )
            else:
                args = moreargs.copy()
            
            if 'kwargs' in response:
                kwargs = response['kwargs'].copy()
                kwargs.update( morekwargs )
            else:
                kwargs = morekwargs
            
            if response['passNumber'] ==True:
                args.insert( 0,  key)
            elif response['passNumber'] != False:
                kwargs[response['passNumber']] = key
                
            if response['passKey'] == True:
                args.insert( 0, self.reverseLookup(key))
            elif response['passKey'] != True:
                kwargs[response['passKey']] = self.reverseLookup(key) 
                
                
            return response['action']( *args, **kwargs )
            
        else:
            return -1 
        
    def disableKey(self, key):
        key = self.translateKey(key)
        
        if key in self.responses:
            self.disabled[key] = self.responses[key]
            del self.responses[key]
        
    def enableKey(self, key):
        key = self.translateKey(key)
        
        if key in self.disabled:
            self.responses[key] = self.disabled[key]
            del self.disabled[key]