#!/usr/bin/python3
# BHDUP VERSION 1.0
import os
import time
import sys
import requests
import guessit
import colorama
from dotenv import load_dotenv
from colorama import Fore, Style
from tqdm import tqdm
from tmdbv3api import TMDb
from tmdbv3api import TV
from tmdbv3api import Movie
from imdb import IMDb
import imdb

# GETTING ENVIRONMENT VARIABLES FROM .ENV FILE
BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))
torrentpasskey = os.getenv("TORRENTPASSKEY")
bhdapi = os.getenv("BHDAPI")
tmdbapi = os.getenv("TMDBAPI")
ss1 = os.getenv("SCREEN_SHOT1")
ss2 = os.getenv("SCREEN_SHOT2")
ss3 = os.getenv("SCREEN_SHOT3")
ss4 = os.getenv("SCREEN_SHOT4")
ss5 = os.getenv("SCREEN_SHOT5")
ss6 = os.getenv("SCREEN_SHOT6")

print(Fore.RED + "Starting BHDUP Script V1" + Fore.WHITE)

# USER INPUT TO DEFINE VARIABLES FOR API POST REQUEST
category = 0
live = 2
pack = 2
anon = 2
while ((category != 1) and (category != 2)):
    category = int(input("Enter 1 for Movie or 2 for TV: "))
while ((pack != 0) and (pack != 1)):
    if category != 2:
        break
    else:
        pack = int(input("Enter 1 if Pack or 0 if not a Pack: "))
while ((live != 0) and (live != 1)):
    live = int(input("Enter 1 for Live torrent or 0 to send to Drafts: "))
while ((anon != 0) and (anon != 1)):
    anon = int(input("Enter 1 if Anonymous or 0 if not Anonymous: "))

# MORE VARIABLES
bhdurl = "https://beyond-hd.me/api/upload/"
url = str(bhdurl + bhdapi)
a = os.listdir()
torrents = sorted(a)
torrents.remove("bhdup.py")
torrents.remove("requirements.txt")
torrents.remove(".env")

# SCREENSHOT FUNCTION
def screen_shots(foldername, filename):
    print(Fore.MAGENTA + "Generating Thumbnails")
    ss_time = [ss1, ss2, ss3, ss4, ss5, ss6]
    i=1
    for time in ss_time:
        os.system("ffmpeg -nostats -loglevel 0 -ss " + time + " -i " + foldername + "/" + filename + "  -vframes 1 -q:v 2 ./" + str(i) + ".png")
        i = i + 1

# START LOOP
print(Fore.WHITE)
for t in tqdm(torrents):

    # CREATE TEMP DIRECTORY
    os.mkdir('./' + t + ".files" '/')
    print(Fore.BLUE + "Processing files for " +t )

    # HASH TORRENT (PIECE SIZE IS 24 WORKS WITH MOST FILE SIZES)
    os.system("mktorrent -p -l 24 -a https://beyond-hd.me/announce/" + torrentpasskey + " -o ./" + t + ".torrent " + t + " > /dev/null 2>&1")
    print(Fore.GREEN + "Torrent Hashed")
    time.sleep(2)

    # DUMP MEDIAINFO
    video = os.listdir(t)
    os.system("mediainfo " + t + "/" + video[0] + " > ./mediainfo.txt")
    print(Fore.YELLOW + "Mediainfo Generated")
    time.sleep(2)
    screen_shots(t, video[0])

    # UPLOAD THUMBNAILS AND SAVE BBCODE TO VARIABLE
    print(Fore.CYAN + "Starting Upload to imgbox")
    os.system("imgbox *.png -w 350 > tmp")
    os.system(r"grep -R 'Webpage\|Thumbnail' tmp | awk -F ' ' '{print $2}' | sed '1~2s/\(.*\)/]\[img]\1\[\/img]\[\/URL]/g ; N;s/\(.*\)\n\(.*\)/\2\1/ ; s/^/\[URL=/' | tr -d '[:space:]' > ./" + t + ".files/bbcode.txt")
    with open("./" + t + ".files/bbcode.txt", "r") as myfile:
        bbcode = str(myfile.readlines())[2:-2]

    # USE GUESSIT TO DEFINE MORE VARIABLES
    guess = dict(guessit.guessit(t))
    searchterm = (guess['title'])
    reso = guess.get('screen_size', None)
    source = (guess['source'])
    other = guess.get('other', None)
    name = str(t.replace(".", " "))

    # JANKY IF STATEMENTS TO MAKE GUESSIT OUTPUT API FRIENDLY
    if "Web" in source:
        source = "WEB"
    elif ((source == "Blu-ray") and (other == "Remux") and (reso == "1080p")):
        reso = "BD Remux"
    elif "DVD" in name:
        reso = "DVD Remux"
    elif ((source == "Ultra HD Blu-ray") and (other == "Remux") and (reso == "2160p")):
        reso = "UHD Remux"
        source = "Blu-ray"

    # SEARCH TMDB AND IMDB APIS FOR GUESSIT TITLE
    tmdb = TMDb()
    tmdb.api_key = tmdbapi
    tv = TV()
    show = tv.search(searchterm)
    for result in show:
        tmdbid1 = str(show[0].id)
    movie = Movie()
    search = movie.search(searchterm)
    for res in search:
        tmdbid2 = str(search[0].id)
    if category == 1:
        tmdbid = tmdbid2
    elif category == 2:
        tmdbid = tmdbid1
    ia = imdb.IMDb()
    im = ia.search_movie(searchterm)
    imdbid = str(im[0].movieID)
    os.system("cp *.torrent ./" + t + ".files/")

    # SEND POST REQUEST TO BHDAPI
    print(Fore.YELLOW + "Uploading torrent to BHD")
    payload={'name':name,
            'description':bbcode,
            'category_id':category,
    	    'type':reso,
    	    'source':source,
    	    'imdb_id':imdbid,
    	    'tmdb_id':tmdbid,
    	    'pack':pack,
    	    'live':live,
    	    'anon':anon}
    torrentfile = "./" + t + ".torrent"
    mediainfofile = "./mediainfo.txt"
    files = {'file': open(torrentfile, 'rb'), 'mediainfo': open(mediainfofile, 'rb')}
    response = requests.request("POST", url, data=payload, files=files)
    print(Fore.GREEN)
    print(response.text)

    # CLEANUP
    os.system("rm *.png tmp* *.torrent mediainfo.txt")
    print(Fore.WHITE + "Finished Processing files for " +t)
    #sys.exit("end of loop break")

# IF LOOP SUCCESSFUL CLEANUP TEMP DIRECTORIES
os.system("mv **/*.torrent ./ && rm -r *.files")
print(Fore.RED + "Torrent Script Successfully Executed!!!")
print(Fore.WHITE)