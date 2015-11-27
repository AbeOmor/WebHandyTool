import subprocess
from bs4 import BeautifulSoup
from urllib2 import *
import datetime
import urllib2
import re
from urllib import urlretrieve

class parsers(object):

    def BS_parse_data(self,link):
        """
        Returns BeautifulSoup object for the link given, this will allow modules parse through pages data much faster

        :param link:
        :return BeautifulSoup :
        """

        try:
            soup = BeautifulSoup(urlopen(link),"html.parser")
        except urllib2.HTTPError:
            soup = 'HTTP Error'

        return soup

    def HTML_text(self,link):
        """
        Returns HTML text data for Query search

        :param link:
        :return String :
        """

        try:
            soup = BeautifulSoup(urlopen(link),"html.parser")
            data = re.sub(r'\n\s*\n', r'\n\n', soup.get_text().strip(), flags=re.M)
        except urllib2.HTTPError:
            soup = 'HTTP Error'
            return soup
        return data