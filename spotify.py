#/usr/bin/python3

import requests
#import ast
import json

# 
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait#, select
from selenium.webdriver.common.proxy import *
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


#import requests
from time import sleep

from secrets import *

#TODO
# ADD FEATURE TO REFRESH TOKEN, IT IS WAY BETTER HAVE NEW TOKEN WHEN OLD ONE EXPIRES
# ADD PLAYLİSTS TO LIKED SONGS
#/TODO



null = 0    # as global variable
            # Since spotify has some vaule null, I had to define it to control loops

#Note: If Web API returns status code 429, it means that you have sent too many requests. When this happens, check the Retry-After header, where you will see a number displayed. This is the number of seconds that you need to wait, before you try your request again.

#
#200 	OK - The request has succeeded. The client can read the result of the request in the body and the headers of the response.
#
#201 	Created - The request has been fulfilled and resulted in a new resource being created.
#
#202 	Accepted - The request has been accepted for processing, but the processing has not been completed.
#
#204 	No Content - The request has succeeded but returns no message body.
#
#304 	Not Modified. See Conditional requests.
#
#400 	Bad Request - The request could not be understood by the server due to malformed syntax. The message body will contain more information; see Response Schema.
#
#401 	Unauthorized - The request requires user authentication or, if the request included authorization credentials, authorization has been refused for those credentials.
#
#403 	Forbidden - The server understood the request, but is refusing to fulfill it.
#
#404 	Not Found - The requested resource could not be found. This error can be due to a temporary or permanent condition.
#
#429 	Too Many Requests - Rate limiting has been applied.
#
#500 	Internal Server Error. You should never receive this error because our clever coders catch them all … but if you are unlucky enough to get one, please report it to us through a comment at the bottom of this page.
#
#502 	Bad Gateway - The server was acting as a gateway or proxy and received an invalid response from the upstream server.
#
#503 	Service Unavailable - The server is currently unable to handle the request due to a temporary condition which will be alleviated after some delay. You can choose to resend the request again.
#
#
#
#


class driver(object):
    def __init__(self):
        #ıt was going to for oauth login, but tidal dedects any selenium activity or being
        #I just created it to automate geting token from spotify

        #_ff_prfl = webdriver.FirefoxProfile()
        #_ff_optn = webdriver.FirefoxOptions()
        
        # 
        # for debugging
        #_ff_prfl.set_preference("layout.css.devPixelsPerPx","0.3") 

        #_ff_optn.set_headless()


        #self._driver = webdriver.Firefox(firefox_profile=_ff_prfl,firefox_options=_ff_optn)
        

        opts = Options() # suggested way to have headless driver
        opts.headless = True
        #opts.set_preference("layout.css.devPixelsPerPx","0.1")

        self._driver = webdriver.Firefox(options=opts)




    def return_driver(self):
        return self._driver





class Spotify(object):

    def __init__(self):

        self.scopes = ["playlist-read-private","playlist-read-collaborative","user-follow-read","user-library-read","user-read-private"]# All scopes, I will add a feature to select scopes you want to use, for now, I use it in fast strings

        self.username = spotify_username
        self.password = spotify_password
        self.client_id = spotify_client_id
        self.client_secret = spotify_client_secret
        self.market = spotify_market
        
        self.redirect_uri = spotify_redirect_uri
        self.driver = 0
        self.token = 0
        self.code_for_token = 0
        self.get_token()


    def _get_driver(self):
        self.driver =  driver().return_driver()
        return 0
        #pass

    def _driver_quit(self):# driver disponse 
        self.driver.quit()
        return 0

    def _driver_close(self):# close currently focused
        self.driver.close()
        return 0



    def _get_code_for_token(self, client_id, client_secret):

        self._get_driver()

        self.driver.get(f"https://accounts.spotify.com/authorize?client_id={self.client_id}&response_type=code&redirect_uri={self.redirect_uri}&scope={self.scopes[0]}%20{self.scopes[1]}")


        # Having a code to access token, user have to interact with app menu, I just automated it Just needed once
        sleep(0.7)
        self.driver.find_element_by_xpath("""//*[@id="login-username"]""").send_keys(self.username)
        self.driver.find_element_by_xpath("""//*[@id="login-password"]""").send_keys(self.password)
        self.driver.find_element_by_xpath("""//*[@id="login-button"]""").click()

        sleep(2)
        print(self.driver.current_url)
        self.code_for_token = self.driver.current_url[32:]
        self._driver_quit()
        return 0

    



    def _get_token(self):

        data = {
            "grant_type"    :   "authorization_code",
            "code"          :   self.code_for_token,
            "redirect_uri"  :   self.redirect_uri,
            "client_id"     :   self.client_id,
            "client_secret" :   self.client_secret,
        }

        r = requests.post("https://accounts.spotify.com/api/token", data = data)
        #{
        #    "access_token": "NgCXRK...MzYjw", new token
        #    "token_type": "Bearer",
        #    "scope": "user-read-private user-read-email",
        #    "expires_in": 3600,
        #    "refresh_token": "NgAagA...Um_SHo" when token expires, use it to refresh it
        #}

        self.token = r.json()["access_token"]#ast.literal_eval(r.text)["access_token"]
        self.code_for_token = r.json()["refresh_token"]#ast.literal_eval(r.text)["refresh_token"]

        return 0

    def get_token(self):
        self._get_code_for_token(self.client_id, self.client_secret)
        self._get_token()
        return 0


    def _get_list_users_playlists(self, offset = 0, limit = 50):
        #Get a list of the playlists owned or followed by a Spotify user.
        #
        #max limit 50
        # "https://api.spotify.com/v1/users/user_id/playlists?limit=50t&offset=0" -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer Token
        #
        #
            
        header = {
            "Accept"        :   "application/json", 
            "Content-Type"  :   "application/json",
            "Authorization" :   f"Bearer {self.token}",

        }
        

        print("\n\n\nUSER ID", self.username)
        print("\n\n\nTOKEN", self.token)
        print("\n\n\nLIMIT", limit)
        print("\n\n\nOFFSET",offset)
        print("\n\n\nHEADER",header)

        
        # parameters are embed to link
        r = requests.get(f"https://api.spotify.com/v1/users/{self.username}/playlists?limit={limit}&offset={offset}", headers = header)


        print(r.status_code) # Print status code to be sure

    
        return r.json()

        #pass


    def write_all_users_playlists(self): # Dump all playlists 
        print("WRITE ALL USERS PLAYLISTS ")
        flag_next = 1
        offset = 0
        items = []

        while(flag_next): # flag returns null when there is no other link, that we get from response of spotify api and null is a global variable equals to 0

            print("FLAG_NEXT", flag_next)
            response = self._get_list_users_playlists(offset)
            
            [items.append(x) for x in response["items"]]
 
            flag_next = response["next"]
            #flag_next = 0
            offset  = offset + 50


        file = open("spotify_playlists.json","a")
        json.dump(items, file)
        file.close()
        return 0


    def _get_playlist_items(self, track_id, offset = 0, limit = 100):

        # Can return max 100 tracks
        # Authorization required
        # playlist id required
        # market required
        #


        header = {
            "Accept"        :   "application/json", 
            "Content-Type"  :   "application/json",
            "Authorization" :   f"Bearer {self.token}",

        }
        
        
        r = requests.get(f"https://api.spotify.com/v1/playlists/{track_id}/tracks?limit={limit}&offset={offset}", headers = header)
        return r.json()

    def write_all_playlists_items(self):
        flag_next = 1
        offset = 0


        
        playlists = open("spotify_playlists.json","r")

        playlists = json.load(playlists)


        #f["description"], f["external_urls"]["spotify"], f["name"], f["owner"]["display_name"], f["id"]
        
        #('descp of track', 'https://open.spotify.com/playlist/tracklink', 'trackname', 'owner.','id')


        json_response = []
        for trackcounter in range(0, len(playlists)):
            
            print("TRACK COUNTER", trackcounter)
            playlist = {
                "name"          :   "", 
                "description"   :   "",# hold descriptiom, spotfiy link, total
                "items"         :   [],
            }

            playlist["name"] = playlists[trackcounter]["name"]

            playlist["description"] = f"\n{playlists[trackcounter]['description']}\n{playlists[trackcounter]['owner']['display_name']}\n{playlists[trackcounter]['external_urls']['spotify']}\n{playlists[trackcounter]['id']}"

            
            offset =0
            flag_next = 1
            while(flag_next):
                print("FLAG NEXT1 ", flag_next)
                response = self._get_playlist_items(playlists[trackcounter]["id"], offset)

                
                for item in response["items"]:
                    #respone["items"][counter]["track"]
                    raw = {
                        "name"  :"",
                        "artists":[],
                    }

                    try:
                        raw["name"] = item["track"]["name"]
                        [
                            (raw["artists"].append(artist["name"])) for artist in item["track"]["artists"]
                        ]
                    except:
                        pass
                    

                    playlist["items"].append(raw)

            
                flag_next = response["next"]
                
                #flag_next = 0
                offset  = offset + 100
            
            json_response.append(playlist)


            #open("spotify_playlists_tracks.json","a").writelines(json.dumps(playlist))

        file = open("spotify_playlist&tracks.json","a")#.writelines(json.dumps(playlist))
        json.dump(json_response, file)
        file.close()
        return 0

        
def main(args=None):
    # just let do spotify to dump your all playlists and tracks
    bot = Spotify()
    bot.get_token()
    bot.write_all_users_playlists()
    bot.write_all_playlists_items()


    return 0

if __name__ == '__main__':
    main()


