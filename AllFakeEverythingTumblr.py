import pytumblr
from secrets import *    #this imports the content in our tumblr_keys.py file

import urllib.request
import requests
import json
from threading import Timer
import time

from random import randint
from random import uniform

import nltk
from nltk.corpus import wordnet as wn
# from pytumblr.helpers import *

# Authenticate via OAuth
client = pytumblr.TumblrRestClient(
    consumer_key,
    consumer_secret,
    token_key,
    token_secret
)

imageAPIKey = "AIzaSyDeAJ1BYrrIaMg-0y4m89BLS20YQ1Nzf2s"

cx = "003135785870325874272%3Aunfqjadyrr0"

nouns = list(wn.all_synsets(wn.NOUN))

def makePost():
    """
    Generatese "fake ___" phrase, makes meme image, and saves image to post to local folder
    """

    #pick random noun
    index = randint(0, len(nouns)-1)
    noun = nouns[index].name().split(".")[0]
    print("fake " + noun)

    getImage(noun, noun, "meme")

    return noun

def getImage(searchTerm, noun, fileName):
    """
    Searches google images with given search term. Makes meme.
    """
    startIndex = '1'
    key = imageAPIKey
    searchUrl = "https://www.googleapis.com/customsearch/v1?q=" + \
        searchTerm + "&start=" + startIndex + "&key=" + key + "&cx=" + cx + \
        "&searchType=image"
    r = requests.get(searchUrl)
    response = r.content.decode('utf-8')
    result = json.loads(response)
    print(searchUrl)
    print(r)
    # print(result)

    imageLink = result["items"][0]["link"]
    print(imageLink)

    makeMeme(noun, imageLink, fileName)

def makeMeme(noun, imageLink, fileName):
    """
    Makes a meme with give image and saves image to local directory
    """

    #get image
    memeLink = "https://memegen.link/custom/FAKE/" + noun.upper() + ".jpg?alt=" + imageLink
    print("meme: " + memeLink)

    #save image
    req = urllib.request.Request(memeLink, headers={'User-Agent': 'Mozilla/5.0'})
    m = open(fileName + '.jpg', 'wb')

    m.write(urllib.request.urlopen(req).read())
    m.close()


def setInterval(func, sec):
    def func_wrapper():
        setInterval(func, sec)
        func()
    t = Timer(sec, func_wrapper)
    t.start()
    return t


def runBot():
    try:
        noun = makePost()

        # image = open('meme.jpg', 'rb')
        if not debug:
            print("Posting!")
            client.create_photo('all-fake-everything', state="published", tags=["fake", noun], data="meme.jpg")
        # image.close()
    except Exception as err:
        print(err)


debug = False
runOnce = False

runBot()
if not runOnce:
    setInterval(runBot, 60*60)        #runs every hour


