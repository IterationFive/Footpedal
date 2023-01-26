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
        
    def clear(self):
        with self.Lock:
            dict.clear(self)
            self.__autosave()
            
    def copy(self):
        with self.Lock():
            return dict.copy(self )

    def get(self, __key, __default):
        with self.Lock:
            return dict.get(self, __key, __default)
        
    def items(self):
        with self.Lock:
            return dict.items(self)
        
    def keys(self):
        with self.Lock:
            return dict.keys(self)
    
    def pop(self, *args):
        with self.Lock:
            r = dict.pop(self,*args)
            self.__autosave()
            return r
        
    def popitem(self):
        with self.Lock:
            r = dict.popitem(self)
            self.__autosave()
            return r
        
    def setdefault(self, key,default):
        with self.Lock:
            r = dict.setdefault(self, key, default)
            if r == default:
                self.__autosave()
             
    def update(self, **kwargs):
        with self.Lock:
            dict.update(self, **kwargs)
            self.__autosave
            
    def values(self):
        with self.Lock:
            return dict.values(self)
        
    def __autosave(self):
        if self.__auto:
            self.__save()
            
    def save(self):
        with self.Lock:
            self.save()
            
    def __save(self, filename=None):
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
                j = json.load(f)
                f.close()
                
                if type( j ) == dict:
                    dict.clear(self)
                    dict.update(self, j)
                    
                    if keepName:
                        self.__file = filename
                else:
                    raise ValueError( 'File ' + filename + ' does not contain a json dictionary' )
                
            else:
                raise ValueError( 'Invalid filename ' + filename + ' supplied to Dictionary' )
            
            
    