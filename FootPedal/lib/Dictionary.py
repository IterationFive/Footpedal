'''
Created on Jan 26, 2023

@author: Cather Steincamp
'''
from os.path import isfile
from threading import Lock
import json

class Dictionary(dict):
    '''
    Dictionary extends the python dictionary in the following ways:
            
        While the dict class is thread-safe for single
        operations, this adds a threading lock for 
        multiple operations.
    
        Adds saving to and/or loading from a json file.      
    
    '''
    
    def __init__(self, file=None, autoSave=False ):
        dict.__init__(self)
        
        self.__file = file
        self.__auto = autoSave
        self.Lock = Lock()
        
        if file is not None and isfile( file ):
            self.load()
        
    def clear(self):
        dict.clear(self)
        self.__autosave()
        
    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        self.__autosave()
    
    def pop(self, *args):
        r = dict.pop(self,*args)
        self.__autosave()
        return r
        
    def popitem(self):
        r = dict.popitem(self)
        self.__autosave()
        return r
    
    def setdefault(self, key,default):        
        r = dict.setdefault(self, key, default)
        if r == default:
            self.__autosave()
        return r
    
    def update(self, **kwargs):
        dict.update(self, **kwargs)
        self.__autosave
            
    def values(self):
        return dict.values(self)
        
    def __autosave(self):
        if self.__auto:
            self.save()
            
    def save(self, filename=None):
        if filename is None:
            filename = self.__file
        
        if self.__file is not None:
            try:
                f = open( filename, 'w' )
            except:
                raise ValueError( 'Invalid filename ' + filename + ' supplied to Dictionary')
            else:
                json.dump(self, f, indent=1)
                f.close()
                    
    def load(self, filename=None, keepName = True ):
        with self.Lock:
        
            if filename is None:
                filename = self.__file
                
            if isfile( filename ):
                
                f = open( filename, 'r' )
                try:
                    j = json.load(f)
                except:
                    j = {}
                    
                f.close()
                
                if type( j ) == dict:
                    dict.clear(self)
                    dict.update(self, j)
                    
                    if keepName:
                        self.__file = filename
                else:
                    raise ValueError( 'File ' + filename + ' does not contain a json dictionary' )
                
            
            
            
    