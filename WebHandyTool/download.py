import subprocess
from bs4 import BeautifulSoup
from urllib2 import *
import datetime
import urllib2
import re
from urllib import urlretrieve

class download(object):

    def download_resources(self,link,options = '-rA', file_type=None):
        """
        Writes all resources matching the given file type from the page link to the file specified by destination.

        :param link:
        :param options:
        :param file_type:
        :return:
        """

        file_type = raw_input("Enter the extension you would like to download: ")
        more_request = raw_input('Do you want more, enter Y or N: ')

        while more_request.lower() == 'y':
            more_file_type = raw_input("Enter the next extension you would like to download: ")
            file_type+= "," + more_file_type
            print file_type
            more_request = raw_input('Do you want to enter more extensions? Enter Y or N:')

        if file_type:
            # Call UNIX wget process to download files
            p = subprocess.call(["wget",options,file_type,link])
        else:
            p = subprocess.call(["wget",options,link])