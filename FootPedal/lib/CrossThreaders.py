'''
Created on Dec 15, 2022

@author: Cather Steincamp

These objects encapsulate and secure individual items, threads, or dictionaries.
if a list or dictionary is passed to these items, or read from (not removed), it
will be copied, rather than passed by reference.

'''

from threading import Lock

class CrossThreader(object):
    def __init__(self):
        self.lock=Lock()
    def copyIfNeeded(self, item):
        if type(item) == list or type( item ) == dict:
            return item.copy()
        else:
            return item

class CrossThreadItem(CrossThreader):
    '''
    classdocs
    '''
    def __init__(self, item ):
        CrossThreader.__init__(self)
        self.item = self.copyIfNeeded( item )

    def get(self):
        with self.lock:
            return self.copyIfNeeded( self.item )

    def set(self, item):
        with self.lock:
            self.item = self.copyIfNeeded( item )
            
class CrossThreadDict(CrossThreader):
    def __init__(self, d:dict=None):
        CrossThreader.__init__(self)
        self.lock = Lock()
        if d is None: 
            self.d = {}
        else:
            self.d = d.copy()

    def get(self, key):
        with self.lock:
            if key in self.d:
                return self.copyIfNeeded( self.d[key] )
            else:
                return False

    def set(self, key, v):
        with self.lock:
            self.d[key] = self.copyIfNeeded( v )
            
    def copy(self):
        with self.lock:
            return self.d.copy()
        
    def replace(self, d:dict ):
        with self.lock:
            self.d = d.copy()
        
    def update(self, d:dict ):
        with self.lock:
            self.d.update(d)
    
class CrossThreadList(CrossThreader):
    def __init__(self, l=None):
        CrossThreader.__init__(self)
        if l is None:
            self.l = []
        else:
            self.l = self.copyIfNeeded( l )
                
    def append(self, addition:list):
        with self.lock:
            self.l.append( addition.copy() )
                                
    def clear(self):
        with self.lock:
            self.l.clear()
            
    def copy(self):
        with self.lock:
            return self.l.copy()
            
    def length(self):
        with self.lock:
            return len( self.l )
                
    def extend(self, addition:list):
        with self.lock:
            self.l.extend( addition.copy() )
            
    def index(self, value):
        with self.lock:
            return self.copyIfNeeded( self.l.index(value))
            
    def insert(self, index, insertion):
        with self.lock:
            self.l.insert( index, self.copyIfNeeded( insertion ) )
    
    def pop(self, index):   
        with self.lock:
            if len( self.l ) > index :
                r = self.l.pop(index)
            else:
                r = None       
        return r
            
    def remove(self, i ):
        with self.lock:
            if i in self.l:
                self.l.remove(i)
    
    def reverse(self):
        with self.lock:
            self.l = self.l.reverse()
            
    def sort(self):
        with self.lock:
            self.l = self.l.sort()
            
    def size(self):
        with self.lock:
            return len( self.l )
            
    def replace(self, l:list):
        with self.lock:
            self.l = l.copy() 
                    
    def add(self, addition):        
        with self.lock:
            if type( addition ) == list:            
                self.l.extend( addition.copy() )
            else:           
                self.l.append( self.copyIfNeeded( addition )  )
                
    def moveItem(self, index, offset):        
        with self.lock:
            
            if len( self.l ) < index or index < 0:
                #index exceeds bounds of l
                return False 
            elif index + offset > -1 :
                #new position exceeds lower bounds of l
                return False 
            elif index + offset < len( self.l):
                #new position exceeds upper bounds of l
                return False 
            
            item = self.l.pop( index )
            self.l.insert( index + offset, item )
            
    def moveItemDown(self, index, offset=1):
        self.moveItem( index, offset )
            
    def moveItemUp(self, index, offset=1):
        self.moveItem( index, 0 - offset )  
            
    def read(self, index):
        with self.lock:
            if index < len( self.l ):
                return self.copyIfNeeded( self.l[index] )                
            else:
                return None
                    
                
        
        