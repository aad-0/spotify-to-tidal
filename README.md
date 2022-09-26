Not very important update:
    since tidal is not available in Turkey, I will not add any further features.

version beta 0.1.0

just run the Spotify first, then run the tidal.py

what do these scripts are dump all playlists with tracks and write them into some files via Spotify API's. Tidal has no service of public API's, but they have a similar API system. You can see some of them in tidal.py

TODO

[]  ADD an OAuth login, Spotify has it, but tidal
    Spotify does login automatically. I just leave it as it is, it will be changed after beta

    Tidal detects any selenium activity or being, so;
        1) I can put a portable any browser, and get all cookies
        2) Make selenium driver undetected

        I will take one of these ways, but it is not my first preference to have a script for dump all cookies for a browser




[]  ADD feature;

    []  sync,
    []  play the same track on both services,
    []  get Spotify weekly playlists,
What secrets.py needs:

    Just add your Spotify username, you can get it via the link:https://www.spotify.com/tr/account/overview/

    market, you can also get this information via link overview

    for client id, client secret and spotify_redirect_uri:
    You have to create an app from the Spotify developer dashboard
    https://developer.spotify.com/dashboard/applications
    log in here and click "Create An App"
    just give a name then you will see Client ID and Client Secret, under "Show Client Secret"
    then click "Edit Settings"
    and add a Redirect URI

    Script gets token automatically


    tidal login and tidal password is not necessary

    the market is, it should be same as Spotifys'

    for Tidal token, when you logged in to listen. Tidal, you have to open developer tools from your web browser, then go to storage and click local storage you have to find oAuthAccessToken
    
Anyone can change source codes, use them as they want. I just do not accept any responsibilities.
