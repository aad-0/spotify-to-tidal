version beta 0.1.0

just run the spotify first, then run the tidal.py

what do these scripts is dump all playlists with tracks and write them into some files via spotify API's.
Tidal has no service of public API's, but they have simular API system. You can see some of them in tidal.py

TODO

    []  ADD a oauth login, spotify has it, but tidal
        Spotify does login automatically. I just leave as it is, it will be changed after beta
    
        Tidal dedects any selenium activity or being, so;
            1) I can put a portable any browser, and get all cookies
            2) Make selenium driver undedected

            I will take one of these ways, but it is not my first preference to have a script for dump all cookies for a browser




    []  ADD feature;

        []  sync,
        []  play same track on both services,
        []  get spotify weekly playlists,




What secrets.py needs:

    Just add your spotify username, you can get it via link:https://www.spotify.com/tr/account/overview/

    market, you can also get this information via link overview

    for client id, client secret and spotify_redirect_uri:
    You have to create a app from spotify developer dashboard
    https://developer.spotify.com/dashboard/applications
    login here and click "Create An App"
    just give a name then you will see Client ID and Client Secret, under "Show Client Secret"
    then click "Edit Settings"
    and add a Redirect URI

    Script gets token automatically


    tidal login, and tidal password is not nececarry

    market is, it should be same as Spotifys'

    for tidal token, when you logged in to listen.tidal, you have to open developer tools from your webbrowser, then go to storage and click local storage you have to find oAuthAccessToken



Anyone can change source codes, use as them as they want. I just do not accept any responsibilities.

