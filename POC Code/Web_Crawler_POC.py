__author__ = 'Abe'

from bs4 import BeautifulSoup
from pprint import pprint
import requests
import urlparse
from urllib2 import urlopen
from urllib import urlretrieve
import os
import sys

class Web_Crawler_POC(object):
    def __init__(self):
        self.start = 'www.example.com'

    """
    Used to get all the links on a page
    """
    def grabLinks(self):
        self.start = raw_input("What website do you what to crawl (Input format = www.example.com):")
        r  = requests.get("HTTP://" + self.start)
        data = r.text
        soup = BeautifulSoup(data,"html.parser")

        for link in soup.find_all('a'):
            print "Found this link on the page :" + link.get('href')

    """
    Used to download the HTML and all the images
    """
    def downloadHTML(self):
        self.start = raw_input("What website do you what to crawl (Input format = www.example.com):")
        URL = "HTTP://" + self.start
        soup = BeautifulSoup(urlopen(URL),"html.parser")
        parsed = list(urlparse.urlparse(URL))
        for image in soup.findAll("img"):
            #Print out the string of the image file being processed
            print "Image: %(src)s" % image
            filename = image["src"].split("/")[-1]
            outpath = os.path.join('imgs/', filename)

            if image["src"].lower().startswith("http"):
                urlretrieve(image["src"], outpath)
            else:
                urlretrieve(urlparse.urlunparse(parsed), outpath)

        print "HTML: " + soup.title.string
        HTMLoutpath = os.path.join('HTML/', str(soup.title.string) + ".html")
        urlretrieve(URL,HTMLoutpath)


if __name__ == '__main__':
    choice = raw_input("Do you want to get all links on site (Enter : l) or download the site (Enter: d) ")

    webcrawl = Web_Crawler_POC()

    if choice.lower() == 'l':
        webcrawl.grabLinks()

    if choice.lower() == 'd':
        webcrawl.downloadHTML()
