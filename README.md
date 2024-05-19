# Tdarr Scanner

An autoscanner similar to [Plex Autoscan.](https://github.com/l3uddz/plex_autoscan) But for [Tdarr](https://home.tdarr.io/) 

This is the source code that was used to make the [dockerized version of this](https://hub.docker.com/r/doesntfazer/tdarrscanner). If you would like to make any modifications to this, it can be done here.
 
## Why does Tdarr scanner exist?
I made this little webhook script because I was sick of Tdarr's automatic scan pulling files before they are finished transferring to my NAS; It will cause corrupted files. There's a couple ways around this. 

 1. You could either set it to scan at a certain interval. Let's say every 30 minutes. This is a good work-around, but you will, at some point, have the scan start when a file is in the middle of transferring.
 
 2. The second option is to use "Hold files after scanning" at the bottom of the library. You could set files not to start the scan until the file has sat for a designated time. With this method, you will still run into the same issue listed in example 1. In addition to issue 1, you have to have a good idea of the amount of time it takes for your files to transfer. 
 
 3. You can use Tdarr Autoscanner. Tdarr autoscanner works in tandem with Sonarr and Radarr, and only starts scanning when the files have finished transferring and importing. You can still run into issues using this method. But they are much more rare.

## Wow, that's great! What do I need to set it up?

 - A working instance of Sonarr, Radarr, and Tdarr. 
 - about 5 minutes.

## Reqirements.
- Docker! 

## Docker-compose Examples

Example:

    version: "2.1"
    services:
      tdarrscanner:
        image: doesntfazer/tdarrscanner
        container_name: tdarrscanner
        restart: unless-stopped
        ports:
          - "5000:5000"
        volumes:
          - /var/run/docker.sock:/var/run/docker.sock
        environment:
          - SONARR_URL=http://Tdarr_TV_Library_URL
          - RADARR_URL=http://Tdarr_Movie_Library_URL
          
You need to change the SONARR_URL and RADARR_URL to the URL of your Tdarr library instance.
Go to your web instance of Tdarr. Go to **Libraries** and select your **Library**. In my case, I would click on **Movies** and/or **TV Shows.** 

***CAUTION***: These are different. You must select each library.

In your address bar, you need tocopy and then paste your URL into SONARR_URL. It will look something like this:

***Example***: 

    environment:
      - SONARR_URL=http://192.168.0.3:8265/#/libraries/l6pK7YCUy/source
      - RADARR_URL=http://192.168.0.3:8265/#/libraries/0WEwzc7OF/source

Then you can run your docker-compose command. 

***Example with Sonarr, Radarr and Tdarr Scanner on the docker compose file***:

    version: "2.1"
    services:
      sonarr:
        image: lscr.io/linuxserver/sonarr:latest
        container_name: sonarr
        environment:
          - PUID=1000
          - PGID=1000
          - TZ=America/New_York
        volumes:
          - /opt/sonarr/data:/config
          - tvshows:/tv #optional
          - /opt/downloadcache:/downloads #optional
        ports:
          - 8989:8989
        restart: unless-stopped
        
        
      radarr:
        image: lscr.io/linuxserver/radarr:latest
        container_name: radarr
        environment:
          - PUID=1000
          - PGID=1000
          - TZ=America/New_York
        volumes:
          - /opt/radarr/data:/config
          - movies:/movies #optional
          - /opt/downloadcache:/downloads #optional
        ports:
          - 7878:7878
        restart: unless-stopped
    
    
      tdarrscanner:
        image: doesntfazer/tdarrscanner
        container_name: tdarrscanner
        restart: unless-stopped
        ports:
          - "5000:5000"
        volumes:
          - /var/run/docker.sock:/var/run/docker.sock
        environment:
          - SONARR_URL=http://192.168.0.3:8265/#/libraries/l6pK7YCUy/source
          - RADARR_URL=http://192.168.0.3:8265/#/libraries/0WEwzc7OF/source

## Sonarr and Radarr setup
1. Open your **Sonarr** and **Radarr** instance. (It is the same instructions for both)
2. Go to **Settings > Connect** and click **Webhook.**
3. Set a **Name**. (I just put tdarrscanner.)
4. Under Notification Triggers ***ONLY*** select **On Import**
5. Under URL put **http://<Tdarr_Scanner_IP_Address>:5000** (Example: **http://192.168.0.3:5000** or **http://tdarrscanner:5000**)
6. Click **Test** and make sure you get a green check mark. Then you **Save**.
