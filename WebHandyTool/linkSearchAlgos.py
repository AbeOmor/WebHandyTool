import subprocess
from bs4 import BeautifulSoup
from urllib2 import *
import datetime
import urllib2
import re
from urllib import urlretrieve
from parsers import parsers
from urlCorrector import *
from config import getConfig


class linkSearchAlgos(object):

    def __init__(self):
        #super(linkSearchAlgos,self).__init__()
        self.urlCorrect = urlCorrector()
        self.HTML_help = HTML_corrector_help()
        self.parser = parsers()
        config = getConfig()
        self.depth_setter(config["depth"])


    def depth_setter(self, depth):
        """
        Sets the default max depth variable for the web crawler
        :param depth:
        :return:
        """

        self.depth = depth

    def bfs(self, link):
        """
        Finds all the links on a give website using the BFS algorithm
        :param link:
        :return A list of all the links found by BFS:
        """

        count = 0
        base_link = self.urlCorrect.HTML_corrector(link)
        current_depth = [link]
        next_depth = []
        links = []
        while count <= self.depth:
            print "Depth " + str(count)
            print "LINKS USED IN DEPTH " + str(count)
            print current_depth
            for link in current_depth:
                links.append(self.urlCorrect.HTML_corrector(link).geturl())
                correct_link = self.urlCorrect.absolute_HTML_corrector(link,base_link).geturl()
                new_links = self.find_links(correct_link)
                if new_links:
                    for link in new_links:
                        next_depth.append(self.urlCorrect.absolute_HTML_corrector(link,base_link).geturl())
                    print "Links on this page: " + str(correct_link) + " HERE is the list: "
                    print new_links

            print "ALL LINKS FOUND IN DEPTH " + str(count)
            print next_depth

            current_depth = next_depth
            next_depth = []
            count += 1
        return links

    def find_links(self,link,destination=None):
        """
        Finds all the links (<a></a> anchor tags on page) on a page, also removes all
        the link that start with '#' or 'data:' as these are not valid urls

        :param link:
        :param destination:
        :return List of Links:
        """

        HTML_corrector_helper = self.HTML_help

        data = self.parser.BS_parse_data(link)
        if data == 'HTTP Error':
            return False
        links = []

        if destination:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M")
            f = open('Found Links at' +timestamp +'.txt','w')
            f.write(data.find_all('a'))
            f.close()

        for link in data.find_all('a'):
            links.append(link.get('href'))

        links = [link for link in links if HTML_corrector_helper.is_link(link)]

        # More understandable version of code above
        #list_of_valid_links = []
        #for link in links:
        #    if self.is_link(link):
        #       list_of_valid_links.append(link)

        return links