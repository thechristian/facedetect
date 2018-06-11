import urllib2
from PIL import Image
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

#global imgWithFacesDirectory
# global urlImgDirectory
global processedImgDirectory

# imgWithFacesDirectory = "ImagesWithFaces/"  # directory to save images with faces
# if not os.path.exists(imgWithFacesDirectory):  # checks if directory exist
#     os.makedirs(imgWithFacesDirectory)

urlImgDirectory= "url_Images/" # directory to save images
# if not os.path.exists(urlImgDirectory):  # checks if directory exist
#     os.makedirs(urlImgDirectory)

# directory for processed images
processedImgDirectory = "url_Images/processed"
if not os.path.exists(processedImgDirectory):  # checks if directory exist
    os.makedirs(processedImgDirectory)

# recursively download images starting from the root URL
def downloadImages(url, level): # the root URL is level 0
    print url
    # initialize count with number of files in processed directory
    xno = glob.glob(os.path.join(urlImgDirectory, 'processed/','*g'))
    count = len(xno)+1
    # size of image to be resized
    size = (500, 500)
    
    global urlList
    if url in urlList: # prevent using the same URL again
        return
    urlList.append(url)
    try:
        urlContent = urllib2.urlopen(url).read()
    except:
        return

    soup = BeautifulSoup(''.join(urlContent), "html.parser")
    # find and download all images
    imgTags = soup.findAll('img')
    for imgTag in imgTags:
        imgUrl = imgTag['src']
        try:
            imgData = urllib2.urlopen(imgUrl).read()
            #fileName = os.path.join(urlImgDirectory, basename(urlsplit(imgUrl)[2]))  # pointing to saving directory
            fim = urlsplit(imgUrl)[2]
            sim = fim.split('/')
            im  = sim[-1]
            filename = os.path.join(urlImgDirectory, im)
            output = open(filename, 'wb')
            # write incomming data from scraping
            output.write(imgData)
            output.close()
            # now convert and rename file
            image = Image.open(filename)
            image.thumbnail(size, Image.ANTIALIAS)

            filename2 = os.path.join(urlImgDirectory, 'processed/', str(count)+'.jpg')
            image.convert('RGB').save(filename2, "JPEG")
            # increment the counter
            count +=1
            # you can choose to delete the images in the url_images root if you want
        except Exception as e:
            print e

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

    data_path = os.path.join('url_Images/processed/', '*g')
    files = glob.glob(data_path)
    allfiles = files[-count:]
    for f1 in allfiles:
        # pass
        identifyFace(f1)
# main
print " "
print ("Images downloaded would be in the working directory")
print "E.g http://yourwebaddress.com"
#time.sleep(5)
print " "

downloadImages(raw_input('Type web url and hit enter to start >> '), 1)


