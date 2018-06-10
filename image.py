import urllib2
#import cv2
import os
import os.path
from os.path import basename
from urlparse import urlsplit
from bs4 import BeautifulSoup # for HTML parsing
import time
from faces import identifyFace
import glob

global urlList
urlList = []
global imgWithFacesDirectory
global urlImgDirectory

imgWithFacesDirectory = "ImagesWithFaces/"  # directory to save images with faces
if not os.path.exists(imgWithFacesDirectory):  # checks if directory exist
    os.makedirs(imgWithFacesDirectory)

urlImgDirectory= "url_Images/" # directory to save images
if not os.path.exists(urlImgDirectory): # checks if directory exist
    os.makedirs(urlImgDirectory)

# recursively download images starting from the root URL
def downloadImages(url, level): # the root URL is level 0
    print url
    global urlList
    if url in urlList: # prevent using the same URL again
        return
    urlList.append(url)
    try:
        urlContent = urllib2.urlopen(url).read()
    except:
        return

    soup = BeautifulSoup(''.join(urlContent))
    # find and download all images
    imgTags = soup.findAll('img')
    for imgTag in imgTags:
        imgUrl = imgTag['src']
        try:
            imgData = urllib2.urlopen(imgUrl).read()
            fileName = os.path.join(urlImgDirectory, basename(urlsplit(imgUrl)[2]))  # pointing to saving directory
            output = open(fileName, 'wb')

            output.write(imgData)
            output.close()
        except:
            pass

    # if there are links on the webpage then recursively repeat
    if level > 0:
        linkTags = soup.findAll('a')
        if len(linkTags) > 0:
            for linkTag in linkTags:
                try:
                    linkUrl = linkTag['href']
                    downloadImages(linkUrl, level - 1)
                except:
                    pass

    data_path = os.path.join(urlImgDirectory, '*g')
    files = glob.glob(data_path)
    for f1 in files:
        identifyFace(f1)
# main
print " "
print ("Images downloaded would be in the working directory")
print "E.g http://yourwebaddress.com"
time.sleep(5)
print " "

downloadImages(raw_input('Type web url and hit enter to start >> '), 1)


