'''
Created on January 21, 2023

@author: Cather Steincamp

'''

import tvdb_v4_official
import re

AIRED = 1
DVD = 2 
ABSOLUTE = 3
ALTERNATE = 4

ORDERTYPES = { 1:'AIRED', 2:'DVD', 3:'ABSOLUTE', 4:'ALTERNATE' }

class TVShow(object):
    '''
    Used to extract episode names from a show.  
    '''

    def __init__(self, series_id, apiKey, pin ):
        '''
        Constructor
        
        series_id is the value from theTVDB.com
        '''
        db = tvdb_v4_official.TVDB( apiKey, pin )
        
        seasons = { AIRED: {}, ABSOLUTE: {}, DVD: {}, ALTERNATE: {} }
        
        try:        
            show = db.get_series_extended( series_id )
        except:
            self.name = False
        else:
            self.name = show['name']
            
            for seasonData in show['seasons']:
                
                seasons[ seasonData['type']['id'] ][seasonData['number']] = {}
                
                rawEpisodeData = db.get_season_extended(seasonData["id"])
                
                for episodeData in rawEpisodeData['episodes']:
    
                    seasons[ seasonData['type']['id'] ][seasonData['number']][episodeData['number']] = episodeData['name']
                
            self.seasons = seasons
        
    def getEpisodeTitleOptions(self, season, episode):
        
        season = int( season )
        episode = int( episode )
        
        titles = {}
        
        for order in ORDERTYPES:
            
            if order in self.seasons and season in self.seasons[order] and episode in self.season[order][season] :
                titles[ ORDERTYPES[order] ] = self.purify( self.season[order][season][episode] )
                
        return titles
                
    def purify(self, r):
        
        r = re.sub( '\?', '', r )
        r = re.sub( '\:', ' -', r )
        r = re.sub( '\?', '', r )
        r = re.sub( '\t', '', r )
        
        return r

    def getOrderOptions(self):
        available = {}
        for order in self.seasons:
            available[ORDERTYPES[order]]=order
        return available

        