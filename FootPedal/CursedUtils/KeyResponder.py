'''
Created on Dec 27, 2022

@author: Cather Steincamp
'''

from CursedUtils.keymaps import KEYMAP, PADTRANSLATOR

class KeyResponder(object):
    '''
    This class is defined to simplify keyboard input under curses, by providing tools 
    to define and manage a set of responses to the use of specific keys and/or a
    default response for keys that are not otherwise defined.  Additionally, it 
    provides several ways to use these responses in your code.
    
    Unless otherwise specified, when configuring a key, one can use either the 
    number that is returned for that key by curses' window.getch(), a single-character
    string representing the key pressed ( e.g. 'a', '!', '5' ), or for non-character 
    keys, the imported KEYMAP provides special strings ( e.g. 'escape','pagedown',
    'backspace', 'padenter' ).
    
    The constructor has three boolean arguments:
            
        caseSensitive
            determines if uppercase letters are treated as different input that their 
            lowercase counterparts.  If True, all uppercase characters will be translated 
            to lowercase when assigned or processed. Defaults to False.
    
        activateKeypad
            By default, curses' window.getch() does not look for keys like home, end, 
            insert, left, pagedown, etc.
            By default, this class DOES, but you can turn it off by setting this to False.  
    
        translateNumpad
            by default curses' window.getch() treats the numpad keys-- the versions of the keypad keys that
            are accessible by turning off numlock-- as different keystrokes.
            by default, this class doesn't, but you can set this to False to get that back.
            
            When this is False, the numpad keys can be differentiated from their counterparts
            by number or by adding 'pad' to the beginning of the string (e.g. 'padleft', 'padinsert')
            
            When true, keys are converted at processing using the imported PADTRANSLATOR
            
            
    Use self.setResponse() to define a response to a given key.  The parameters are:
     
        key
            the number, character, or keymap string corresponding to the keystroke to which we 
            want to respond, or 'default'
            
        action
            the function (passed as reference!) to run when they key is pressed
            
        passKeystroke
            if True, will pass the character or keymap string to the action
            as the first parameter
            
            if a string, will pass it as a keyword argument, using the provided string as the keyword
            
        passKeyNumber
            if True, will pass the number corresponding to the keystroke as the first parameter 
            (or second, if for some reason you're using passKeystroke as well)
            
            if a string, will pass it as a keyword argument, using the provided string as the keyword            
            
        args 
            list or None
            Any arguments here will be passed to the action in the order provided.  If passKeystroke or 
            passKeynumber is True, then those arguments will come first.
            
        kwargs
            dict or None
            This dictionary (if present) will be passed to the action as keyword arguments. Note that 
            any of the keywords in this dictionary that conflict with a keyword used for
            passKeystroke or passKeynumber will be ignored in favor of the key. 
            
    Assigned responses can be managed with the following functions:
        
        clearResponse( key )
            permanently removes the response assigned to the key.
        
        disableResponse( key )
            moves the response to the disabled dictionary, where it can be easily enabled with...
            
        enableResponse( key )
            ...which moves the response back into the dictionary of responses
            
    If a response is on the disabled list, it is possible to assign another response to the
    same key, and then overwrite the new response by re-enabling the key.  (Alternately, if 
    you disable a key while there is a response already disabled, it will overwrite the disabled response.)
    
    Additionally, one can set up aliases, which causes the system to recognize one keypress 
    as another.  Applications of this include assigning multiple keys to do the exact same thing,
    or setting certain characters to be case insensitive without making it a global setting. 
        
        setAlias( pressThisKey, butReportThisKey )
            I have never been prouder of a set of variable names.  
            
        clearAlias( key )
            where 'key' is the key from 'pressThisKey'
        
    Once an alias is assigned, this class will not be able to distinguish between the key pressed
    and the alias assigned to it.  Any response assigned to 'pressThisKey' will be ignored.
    
    In order to prevent management of a single object from getting out of hand, the recommended 
    practice is to create separate objects for each context.  The following methods exist to 
    help reinventing-- or more accurately-- reconfiguring the wheel.
    
        copy()
            returns a new instance that is identical to itself, but independent-- changes made 
            to one will not be reflected in the other.
        merge( keyResponder )
            takes the assigned and disabled responses as well as the aliases from another instance 
            and copies them into itself via dict.update(), with all the overwriting that implies.
            
    There are two (and a half) ways of actually processing keystrokes.  All of them have the capacity 
    to provide additional positional or keyword arguments.  It is important to note that while positional 
    arguments provided here will follow any arguments provided at assignment, keyword arguments can 
    potentially override keyword arguments provided at assignment.  The exception(s) to this are the 
    keywords (if any) provided to pass the keynumber ot key string along to the action, which will 
    override anything else.
    
        keyRespond(  window, nodelay, *moreargs, **morekwargs )
        
            window
                a curses window object or an encapsulating object with the methods 
                getch(), nodelay(), and keypad().
            
            nodelay
                boolean.  is passed to the window.nodelay() method.
                If False, will wait for a keypress.
                If True, will return -1 if no key is pressed.
                            
            responds to a single keypress (or, optionally, the lack thereof).
            
            Will activate or deactivate the keypad according to self.activateKeypad.
            
            Returns True if an action was triggered, False if a key was pressed but no action was 
            triggered, and -1 if no key was pressed (and nodelay was set to True).
        
        
        keyLoop(window, exitKey, iterator, *moreargs, **morekwargs) 
            
            window 
                a curses window object or an encapsulating object with the methods 
                getch(), nodelay(), and keypad().
            
            exitKey
                default is 27 ('escape')
                a single key, or a list of keys, that will terminate the loop.  Note that 
                actions can still be assigned to an exitKey, and will be executed before the loop
                is terminated.
                
                if you don't actually want an exit key, simply assign this a negative number or False, 
                but that's something you should CHOOSE so it's not the default
            
            iterator
                optional method or function. if provided, will run when a key is NOT pressed.
                the iterator will receive any arguments provided by *moreargs and/or **morekwargs.
        
            This continues processing keystrokes until the key defined as 'exitKey' is pressed.  
            
            Will activate or deactivate the keypad according to self.activateKeypad.
            
            Additionaly, if an action has access to this object, it can set the attribute 
            'keepLooping' to False to break the loop.  The flag will be reset the next
            time this method is executed.
        
        respond( key, *moreargs, **morekwargs )
            
            'key', in this case, is SPECIFICALLY the number of the key that has been pressed. 
            
            This one is the 'half', as it does not have the ability to activate the keypad keys, nor 
            does it actually monitor for a keypress.  This method is mostly something for the other 
            two to use, but it's here if you wanted to, for example, run a single keystroke through 
            multiple keyResponder instances until you get a match. 
            
            If an action was triggered, the number of the key will be stored as self.lastKey and 
            True will be returned.  If not, False will be returned and self.lastKey will not be modified.
    
    The last key that triggered an action can be accessed with self.getLastKey().  If you 
    want the key converted to a string, use self.getLastKey(True).        
    
    '''


    def __init__(self, caseSensitive=False, activateKeypad=True, translateNumpad=True):

        self.caseSensitive=caseSensitive
        self.activateKeypad=activateKeypad
        self.translateNumpad=translateNumpad
        
        self.lastKey = False
        
        self.responses = {}
        self.aliases = {}
        self.disabled = {}
        
    def setResponse(self, key, action, passKeystroke=False, passKeyNumber=False, args=[], kwargs={}):
        
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
            
    def clearAll(self):        
        self.responses = {}
        self.aliases = {}
            
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
            
    def clearAlias(self, key):
        
        key = self.translateKey(key)
        if key in self.aliases:
            del self.aliases[key]
            
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
            
            sets self.lastKey if an action is executed
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
                
        self.lastKey = key
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
                self.respond(key, *moreargs, **morekwargs)
                
                if key == exitKey or ( type( exitKey) == list and key in exitKey ):
                    break
                
            elif iterator is not None:
                iterator( *moreargs, **morekwargs)
                
            
    def getLastKey(self, convert=True):
        
        if self.lastKey == False:
            return False
        
        if convert:
            return self.translateKey(self.lastKey)
        else:
            return self.lastKey
        
        
        
        
        
        