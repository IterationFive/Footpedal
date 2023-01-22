'''
Created on Jan 15, 2023

@author: Cather Steincamp
'''
import CursedUtils as cu
import json
import os 

from FootPedal import MAINCONFIG



class ConfigMenu(cu.Window):
    '''
    This class can be used by itself to create and manage simple configuration
    options held as a dictionary (that may or may not contain sub-dictionaries) 
    and stored in a JSON file.
        
        parent: 
            a cursedUtils.Screen object.
        
        tablespacing:
            default 1
            the distance in lines between items in the menu.  The default
            of 1 places a line between each item.  
            Eventually this will default to zero, but I'll
            have other code to update for that.
        
        configFile
            the JSON file where the data will be stored in a pretty indented fashion.
            
    Configuration is done with the .addField() command.  Recommended usage is that 
    each menu be a child class, where .setup() (automatically run by cu.Window's constructor) 
    is basically a collection  of .addField() commands.  Its parameters are as follows:
        
        label
            this is both the onscreen label and the dictionary key for the value
        width
            max width in characters
        description
            optional
            if provided, this text will be displayed in the 'detail' field
        validator
            optional
            a function or method that takes input and tests it to make
            sure it meets desired standards.  A validator should return
            True or an error string, which will be displayed on screen. 
            
    A line of text can be added using .addText(text).
    
    Once configured the menu can be invoked with .runMenu() or .firstRun().  
    
    .firstRun() walks the user through each field, saves the results, then
    runs .runMenu()
    
    .runMenu() lets the user pick which, if any, fields to change, then
    Save and Exit (with S/s) or cancel (Esc).
    
    
    Additional methods:
                
        .isFile(validate) 
        .isDir(validate)
        
            These are built-in validators that test to see whether something 
            is an existing file or directory, respectively
            
        .isFileOrNone(validate)
        .isDirOrNone(validate)
            
            Same as the above, except allows for blank entries.
            
        .layout()
        
            uses the provided title and fields to display the options and
            values on the screen and adds the approriate numbers to the key
            repsonder, along with the save/exit options.
            
            If any values are not in the config dictionary, these values will 
            be initalized with blanks.
            
            does not add the numbers or invoke the key responder; those
            are handled by .runMenu()
            
            This is not a particularly flexible method, but there is nothing
            to prevent it from being overwritten in a child class.
            
        .loadConfig()
        
            is called during initialization; loads the file into the local configuration
            dictionary for editing.
            
            if the file does not exist, it will be created.
        
        .saveConfig()
        
            if any changes have been made, this will rewrite the configuration file.
            
        .saveAndExit()
            the default option for saving and exiting.
            
            (Note that there is no 'cancel' function, as it requires no action, and
            the keyresponder exits on Escape by default.)
            
        .editField(index)
            nust be run after .layout().
            
            This adds the description (if present) to the screen, then creates the editbox 
            and validates the results.  If results fail validation, error message is shown
            and the user is prompted again
            
        .fillSlots()
            utility function to populate the slots of the layout with the corresponding
            configuration values.
            
            
    
    
    '''

    def __init__(self, parent:cu.Screen, tableSpacing = 1, configFile=MAINCONFIG):
        
        self.configFile=configFile
        self.tableSpacing = tableSpacing
        self.fields = []
        self.maxField = 0
        self.maxLabel = 0
        self.keys = cu.KeyResponder()
        self.changed = False
        self.loadConfig()
        cu.Window.__init__(self, parent)
        
    
    def loadConfig(self):
        if os.path.isfile( self.configFile):
            f = open( self.configFile, 'r' )
            self.config = json.load( f )
            f.close()
        else:
            #create an empty file
            self.config = {}
            self.saveConfig()
            
        self.changed = False
        
    def saveConfig(self):
        if self.changed:
            f = open( self.configFile, 'w' )
            json.dump(self.config, f, indent=1)
            f.close()
        self.changed = False
        
    def addText(self, text):
        self.fields.append( ['False', text] )
        
    def addField(self, label, width, description='', validator=None):
        self.fields.append( [label, width, description, validator])
        if width > self.maxField:
            self.maxField = width
        if len( label ) > self.maxLabel:
            self.maxLabel = len( label )
            
    def isFile(self, validate ):
        if os.path.isfile( validate ):
            return True
        else:
            return 'Invalid File Name'
        
    def isFileOrNone(self, validate):
        
        if validate == '': 
            return True
        else:
            return self.isFile( validate )
    
    def isDir(self, validate):
        if os.path.isdir( validate ):
            return True 
        else:
            return 'Invalid Path Name'
        
    def isDirOrNone(self, validate):
        
        if validate == '': 
            return True
        else:
            return self.isDir( validate )
    
    def layout(self):
        
        self.setSlot( 'menutitle', 1, int( self.sizeX / 2 ) - 35, 70, cu.CENTER)
                
        self.slotWrite( 'menutitle', self.title )
        
        self.leftpoint = int( ( self.sizeX - ( self.maxLabel + self.maxField + 5 ) ) / 2 )
        # The five is to account for the option key + 2 spaces each between columns
        
        labelanchor = self.leftpoint + 3 + self.maxLabel
        # The three is to account for the option key and the two spaces after it.
        # note that this is a RIGHT anchor 
        
        fieldanchor = labelanchor + 2 
        
        self.setSlot('detail', 3, 1, self.sizeX - 2, cu.CENTER)
        self.setSlot('error', 5, 1, self.sizeX - 2, cu.CENTER)
        
        self.tableY = 7
        
        y = self.tableY
        
        i = 0
        
        while i < len( self.fields ):
            
            field = self.fields[i]
            
            if field[0] == False:
                x = int( ( self.sizeX - len(field[1]) ) / 2 ) 
                self.write( y, x, field[1] )
            else:
                self.write( y, labelanchor - len( field[0]), field[0])
                self.setSlot( field[0], y, fieldanchor, field[1] )
                self.keys.setResponse( str(i+1), self.editField, args=[i] )
            
            i += 1
            y += self.tableSpacing + 1
            
        self.setSlot( 'menuoption1', y, 1, self.sizeX - 2, cu.CENTER )
        self.setSlot( 'menuoption2', y+1, 1, self.sizeX - 2, cu.CENTER )
        
        self.keys.setResponse( 'S', self.saveAndExit )
        self.keys.setResponse( 's', self.saveAndExit )
        
        # Esc is the default exit key, so it need not be defined here
        
        self.fillSlots()
            
    def firstRun(self):
        self.layout()
    
        i = 0
        
        while i < len( self.fields ):
            self.editField(i)
            i += 1
            
        self.saveConfig()    
        self.runMenu(False)
            
    def runMenu(self, doLayout=True ):
        
        if doLayout:
            self.layout()
            
        i = 0
        y = self.tableY
        
        while i < len( self.fields ):
            self.write( y, self.leftpoint, str(i+1))
            y += self.tableSpacing
            i += 1
            
        self.slotWrite( 'menuoption1', 'Press a number to change the corresponding value' )
        self.slotWrite( 'menuoption2', 'Press S to Save and Exit    Press Esc to Cancel' )
        
        self.keys.keyLoop(self.window)
        
        
    def saveAndExit(self):
        self.saveConfig()
        self.keys.keepLooping = False

    def editField(self, index ):
        # we have been conveniently provided the index of the field in self.fields.
        
        field = self.fields[index]
        slot = self.slot[field[0]]
        
        if self.configKey is None:
            if field[0] not in self.config:
                self.config[field[0]] = ''
                self.changed = True
            
            prefill = self.config[field[0]]
        else:
            if self.configKey not in self.config:
                self.config[self.configKey] = {}
                self.changed = True
            if field[0] not in self.config[self.configKey]:
                self.config[self.configKey][field[0]] = ''
                self.changed = True
                
            prefill = self.config[self.configKey][field[0]]
            
        self.slotWrite('detail', field[2], True )
        
        while True:
        
            r = self.lineInput( slot['y'], slot['x'],slot['w'], prefill )
            
            if field[3] is not None:
                
                validate = field[3](r)
                
                if validate != True :
                    self.slotWrite( 'error', validate, True )
                    prefill = r
                    continue
            
            # either there is no validation or we've passed it
            break
        
        if self.configKey is None:
            if self.config[field[0]] != r:
                self.config[field[0]] = r
                self.changed = True
        else:
            if self.config[self.configKey][field[0]] != r:
                self.config[self.configKey][field[0]] = r
                self.changed = True 
                
        self.slotBlank('error')
        self.slotBlank('detail')
        self.slotWrite(field[0], r, True ) 
        
        
    def fillSlots(self):
        
        if self.configKey is None:
            for field in self.config:
                if type( self.config[field] ) == str and field in self.slot:
                    self.slotWrite( field, self.config[field] )
                    
        elif self.configKey in self.config:
            for field in self.config[self.configKey]:
                if field in self.slot:
                    self.slotWrite(field, self.config[self.configKey][field])
                
        else:
            # if we're being asked for it, we'll need it.
            self.config[self.configKey] = {}
                
            
        
        