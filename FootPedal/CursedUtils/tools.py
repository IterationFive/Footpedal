'''
Created on Dec 24, 2022

@author: Cather Steincamp
'''

def collapseList(theList):
    '''
    takes a list of [a,b,[c,d],e,[f,[g,h]]] and turns it into [a,b,c,d,e,f,g,h]        
    '''
    
    collapsedList = []
    
    for item in theList:
                    
        if type( item ) == list:
            
            for subitem in item:
                
                if type( subitem ) == list:
                    
                    collapsedList.extend( collapseList( subitem ) )
                    
                else:
                    collapsedList.append( subitem )
        else:
            collapsedList.append(item)
            
    return collapsedList

def collapseSubLists(theList):
    '''
    only collapses secondary lists, so
    
    [a, [b,c, [d,e] ,f] ,[g,h] ] becomes [a, [b,c,d,e,f], [g,h] ]
    '''
    l = []
    for item in theList:
        if type( item ) == list:
            l.append( collapseList(item))
        else:
            l.append(item)
    return l
    
    

def clippedList(theList, maxLength ):
    ''' 
        any item in theList that is longer than maxLength will be truncated.
        any list will be processed recursively and include as a list.
    '''    
    
    
    outputList = []
    
    for item in theList:
        
        if type( item ) == list:
            # must processed recursively
            outputList.extend( clippedList(item, maxLength) )                
        elif len( item ) > maxLength:
            outputList.append( item[0:maxLength] )
        else:
            outputList.append( item )
            
    return outputList

def wrappedList(theList, maxLength ):
    '''        
        Takes theList, which is a list of strings, and returns a list
        where any strings longer than maxLength have been split 
        into a list of strings that meet the criteria.
        
        For example:                      
            outputList( ['short', 'small', 'tiny', 'actually kinda freaking large'] , 15 )                
        would return
            ['short', 'small', 'tiny', [ 'actually kinda', 'freaking large' ] ]
            
            
        note that this will recurse into lists included in the List.
    
    '''
    
    outputList = []
    
    for item in theList:
        
        if type( item ) == list:
            # must processed recursively                
            item = wrappedList(item, maxLength)
            outputList.append( item )
            
        elif len( item ) > maxLength:
            
            linelist = []
            nextline = ''

            wordlist = item.split()
            
            while len( wordlist ) != 0 :
                
                if len( wordlist[0] ) > maxLength:
                    #split it into confirming lengths,
                    #add it to the beginning of the list                      
                    wordlist = splitWord( wordlist[0] ).extend( wordlist )
                    
                if len( nextline ) + len( wordlist[0] ) + 1 > maxLength:
                    linelist.append(nextline) 
                    nextline = ''

                if nextline != '':
                    nextline += ' '
                    
                nextline += wordlist.pop(0)
                
            linelist.append( nextline )
            outputList.append( linelist )
        else:
            outputList.append( item )
            
    return outputList
            
                    
                 
                
        
def splitWord(word, length):
    words = []
    
    for i in range(0, len(word), length) :
        words.append( word[0+i:length+i] )
    return words
        
                
def stringifyList(listYouWantToBeStrings:list ):
    
    for i in range( 0, len( listYouWantToBeStrings ) ):
        
        if type( listYouWantToBeStrings[i] ) not in [str, list]:
            listYouWantToBeStrings[i] = str( listYouWantToBeStrings[i] )
        
def getLongestLength(listOfStrings ):
    '''
        By executing this code, you confirm that you are not Anish Kapoor, 
        you are in no way affiliated to Anish Kapoor, you are not executing 
        this code on behalf of Anish Kapoor or an associate of Anish Kapoor. 
        To the best of your knowledge, information and belief this code will 
        not make its way into the hands of Anish Kapoor.
    '''
    
    longestLength = 0
    
    for item in listOfStrings:
        
        if type( item ) == list:
            thisLength = getLongestLength( item )
        else:
            thisLength = len( item )

        if thisLength > longestLength:
            longestLength = thisLength
            
    return longestLength