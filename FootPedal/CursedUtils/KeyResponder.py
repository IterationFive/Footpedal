'''
Created on Dec 27, 2022

@author: Cather Steincamp
'''

from CursedUtils.keymaps import KEYMAP, PADTRANSLATOR

class KeyResponder(object):
    '''
    This class is defined to simplify the use of keys in curses.
    
    Additional documentation is available with the methods,
    but this section will provide an overview to place the
    functions in the context of the whole.
    
    A response can be assigned to any keystroke by number or using 
    the keys of the imported KEYMAP, and is basically a dictionary 
    containing an action-- which is a function or method-- and any
    positional or keyword arguments.  
    
    The number of the key pressed or a string representation can be 
    passed to the action as a positional or keyword argument if
    so specified during assignment.  Additional positional and/or 
    keyword arguments can also be provided during assignment.
    
    Aliases can be configured for situations where you want the 
    system to respond to one key as if you pressed another key-- 
    for example, if you want only certain letters to be case 
    insensitve.  If you set 'A' as an alias to 'a', then anytime 
    you press A, this class will interpret it as 'a'.  It is 
    important to note that if you do this, there will be no way
    to determine which of the two keys was pressed.  If you 
    need that kind of granularity, assign the same response to
    both keys and pass the key to the action.
    
    Assignments can be disabled without being deleted, allowing
    one to define a wide range of responses that can easily be
    enabled and disabled as needed.
    
    The constructor has three arguments:
            
        caseSensitive
            determines if uppercase letters are treated as different 
            input that their lowercase counterparts.  If true, all 
            uppercase characters will be translated to lowercase when 
            assigned or processed. 
    
        activateKeypad
            boolean
            by default, curses' window.getch() does not look for
            keys like home, end, insert, left, pagedown, etc.
            by default, this class DOES, but you can turn
            it off by setting this to False.
    
        translateNumpad
            determines if the numpad version of the keys will be 
            treated the same as their counterparts. Defaults
            to true.  
            Uses PADTRANSLATOR from the keymap file.
    
    There are three ways to get and process a keystroke.  All three
    give the ability to provide additional positional or keyword 
    arguments that can be passed to ALL responses.  
    
      
    keyLoop(window, exitKey, iterator, *moreargs, **morekwargs) 
    
        This continues processing keystrokes until the key defined 
        as 'exitKey' (by default, 'escape') is pressed.  
        
        Additionaly, if the action has access to this object,
        it can set the property keepLooping to False to 
        break the loop.  The flag will be reset the next
        time this method is executed.
        
        window 
            a curses window object or an encapsulating object
            with the methods getch(), nodelay(), and keypad().
        
        exitKey
            see above.  can be defined with the number or keymap key, 
            or as a list of either.
        
        iterator
            optional. if provided, will run when a key is NOT pressed.
            
        any additional arguments or keyword arguments will be passed 
        to the action and/or, if provided, the iterator.
        
    keyRespond(  window, nodelay, *moreargs, **morekwargs )
    
        This responds to a single keypress, and can be used 
        when you want more control over a loop than provided
        by keyLoop.  
        
        Will activate the keypad keys if desired.
        
        Returns True if an action ws triggered, False if a key
        was pressed but no action was triggered, and -1 if no 
        key was pressed (and nodelay was set to True).
    
        window
            a curses window object or an encapsulating object
            with the methods getch(), nodelay(), and keypad().
        
        nodelay
            boolean.  is passed to the window.nodelay() method.
            If False, will wait for a keypress.
            If True, will return -1 if no key is pressed.
            
        any additional arguments or keyword arguments will be passed 
        to the action.    
        
    respond( key,  *moreargs, **morekwargs )
    
        This is actually called by both of the above methods,
        and does not actually look for the keystroke-- it
        just responds to a number.  This is the ultimate
        build-your-own-code block, but be advised that, since
        it does not actually interact with the window, 
        it does not activate the keypad keys.
        
        if the value of key is a key that has a repsonse,
        the key will be stored as the number in the attribute
        'lastKeyNumber' and as a string in 'lastKeystroke'.
            
    
    '''


    def __init__(self, caseSensitive=False, activateKeypad=True, translateNumpad=True):

        self.caseSensitive=caseSensitive
        self.activateKeypad=activateKeypad
        self.translateNumpad=translateNumpad
        
        self.lastKeyNumber = False
        self.lastKeystroke = False
        
        self.responses = {}
        self.aliases = {}
        self.disabled = {}
        
    def setResponse(self, key, action, passKeystroke=False, passKeyNumber=False, args=[], kwargs={}):
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
        
        if key != 'default':
            key = self.translateKey(key)
                
        if key != False:
            
            if key != 'default' and self.caseSensitive == False and key > 64 and key < 91 : #65-90 is A-Z
                key += 32 
            
            response = { 'action': action  }
            
            if passKeystroke != False:
                response['passKeystroke'] = passKeystroke
            if passKeyNumber != False:
                response['passKeyNumber'] = passKeyNumber
                
            response['args'] = args
            response['kwargs'] = kwargs
                
            self.responses[key] = response
            
    def clearResponses(self, key):        
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
            r.response[key] = self.responses[key].copy()
        for key in self.disabled:
            r.disabled[key] = self.disabled[key].copy()
            
            
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
                
            returns boolean indicating whether an action was executed
            
            sets self.lastKeynumber and self.lastKeystroke if an action is executed
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
            return False
            
        if 'args' in response:
            args = response['args']
            args.extend( moreargs )
        else:
            args = moreargs.copy()            
            
        
        if 'kwargs' in response:
            kwargs = response['kwargs'].copy()
            kwargs.update( morekwargs )
        else:
            kwargs = morekwargs
        
        if 'passKeyNumber' in response:
            if response['passKeyNumber'] ==True:
                args.insert( 0,  key)
            elif response['passKeyNumber'] != False:
                kwargs[response['passKeyNumber']] = key
                
        if 'passKeystroke' in response:
            if response['passKeystroke'] == True:
                args.insert( 0, self.reverseLookup(key))
            elif response['passKeystroke'] != True:
                kwargs[response['passKeystroke']] = self.reverseLookup(key) 
                
        self.lastKeyNumber = key
        self.lastKeystroke = self.reverseLookup(key)
        response['action']( *args, **kwargs )    
        return True
    
    def keyRespond(self, window, nodelay=False, *moreargs, **morekwargs):
        '''
        actually checks for the keypress itself, and then passes that response
        on to response().
        
        activates the keypad if self.activateKeypad is true.
        
        if nodelay is False, will wait for a keypress, and will return False 
        if they key pressed does not have a response.  Will return True if a response
        is triggered (including 'default').
        
        if nodelay is True, will not wait for a keypress.  Will return -1 if
        no key is pressed, or False if the key pressed does not have a response. Will 
        return True if a response is triggered (including 'default').
        '''
        
        window.nodelay(nodelay)
        window.keypad( self.activateKeypad)
        
        key = window.getch()
        
        if key == -1:
            return -1
        
        return self.respond(key, *moreargs, **morekwargs)
        
    def keyLoop(self, window, exitKey=27, iterator=None, *moreargs, **morekwargs ):
        
        if type( exitKey ) == list:
            i = 0
            while i < len( exitKey ):
                exitKey[i] = self.translateKey(exitKey[i])
                i += 1
        else:
            exitKey = self.translateKey(exitKey)
            
        window.keypad( self.activateKeypad)        
        
        if iterator is not None:
            window.nodelay( True )
        else:
            window.nodelay( False )            
        
        self.keepLooping = True
        
        while self.keepLooping:
        
            key = window.getch()
            
            if key != -1:
                self.respond(key, *moreargs **morekwargs)
                
                if key == exitKey or ( type( exitKey) == list and key in exitKey ):
                    break
                
            elif iterator is not None:
                iterator( *moreargs, **morekwargs)
                
            
        
        
        
        
        
        
        