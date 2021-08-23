#/usr/bin/python3


import requests

import json

# 
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait#, select
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

#TODO
#add oauth login to tidal
#   add get playlilsts so also be able to move to spotify
    #GET user playlists list
	#https://api.tidal.com/v2/my-collection/playlists/folders?folderId=root&includeOnly=&offset=0&limit=50&order=DATE&orderDirection=DESC&countryCode=TR&locale=en_US&deviceType=BROWSER
#TODO

#import requests
from time import sleep

import secrets

class Tidal(object):


    #
    def __init__(self):
        self.username = secrets.tidal_login
        self.password = secrets.tidal_password
        self.token = secrets.tidal_token

        self.countryCode = secrets.tidal_country_code
        #pass

    def _read_from_file(self,fname = "spotify_playlist&tracks.json"):
        playlists = json.load(open(fname,"r"))

        return playlists



    def _search(self, query, limit = 15, offset = 0):

        headers = {
            'authorization': f"Bearer {self.token}",
        }
    
    
        params = (
            ('query', query), # query -> aash kaash 1nonly, libubblehum
            ('limit', limit),
            ('offset', offset),
            ('countryCode', self.countryCode),
           
        
        )
        




        r = requests.get('https://listen.tidal.com/v1/search/top-hits', headers=headers, params=params)

        return r.json()

    def _get_list_users_playlists(self, offset = 0, limit = 50):

        headers = {
            'authorization': f"Bearer {self.token}",
        }
        
        params = (
            ('folderId', 'root'),
            ('includeOnly', ''),
            ('offset', '0'),
            ('limit', '50'),
            ('countryCode', self.countryCode),
        )
        
        r = requests.get('https://api.tidal.com/v2/my-collection/playlists/folders', headers=headers, params=params)
    

        return r



    def _create_playlist(self, playlist_name = "Title", playlist_description = "description"):

 
        headers = {
            'authorization': f"Bearer {self.token}",
        }

        params = (
            ('name', f"{playlist_name}"),
            ('description', f"{playlist_description}"),
            ('folderId', 'root'),
            ('countryCode', self.countryCode),
        )

        r = requests.put('https://api.tidal.com/v2/my-collection/playlists/folders/create-playlist', headers=headers, params=params)
        return r#return 0
      
    def _add_to_playlist(self, playlistid, trackid ): # string, array
        

        headers = {
            'Referer': f"https://listen.tidal.com/playlist/{playlistid}",
            'authorization': f"Bearer {self.token}",
            'if-none-match': "*",
        }
        
        
        data = {
          'trackIds': trackid, # can get a list "id1, id2"
        }
        
        r = requests.post(f"https://listen.tidal.com/v1/playlists/{playlistid}/items", headers=headers, data=data)
        return r
        

    def search(self, track_name, artists, searchfor = None): # string, list
        #Search for:
        #, artists
        #, albums
        #, playlists
        #, tracks
        #, videos
        #, genres
        #, tophits

        query =  f"{track_name}"
        for artist in artists:
            query = f"{query} {artist}"
        print("QUERY", query)
        
        search_result = self._search(query=query)
        
        if(searchfor):
           
            #print("returned: ", searchfor)
            return search_result[searchfor]
        
        else:
            #print("returned: ", searchfor)
            return search_result
            

    def move_playlists(self):

        playlists = self._read_from_file()
        

        for playlist in playlists:
            print("__________CREATING PLAYLIST__________",playlist["name"])
            # create playlist

            #tracks = []
            trackids = ""
            
            playlistid = self._create_playlist(playlist["name"], playlist["description"]).json()["data"]["uuid"]
            
            for track in playlist["items"]:
                # search for track
                #return track
                r = self.search(track["name"], track["artists"], "tracks")["items"]

                #return list_raw
                try:
                    
                    trackids = trackids + "," + str(r[0]["id"])
                    #trackid = r[0]["id"]
                except Exception as e:
                    print("Exception ", e)
                    try:
                        trackids = trackids + "," + r["id"]
                        #trackid = r["id"]
                    except Exception as e :
                        print("Exception ", e)
                        print("COULD NOT FOUND THE ", track["name"])
                        

                
                #if(len(trackids.split(",")) == 50):
                #    
                #    print("TRACK IDS ", trackids)
                #    self._add_to_playlsit(playlistid, trackids)
                #    trackids = ""
                #
                #self._add_to_playlsit(playlistid, trackids)


            self._add_to_playlist(playlistid, trackids)



def main(args=None):
    bot = Tidal()
    bot.move_playlists()


if (__name__ == "__main__"):
    main()
