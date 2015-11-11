__author__ = 'Abe'
import urlparse
import sys
import posixpath
import re
import urlparse
from urllib import quote
import SimpleHTTPServer
import SocketServer
from urllib2 import HTTPError
import Queue
import os
import subprocess





class Web_Crawler(object):
    """
    Main class, it is for crawling.
    Class variable includes depth,algo,chocies,choice,output,seed,list of links
    """
    def __init__(self):
        self.depth = self.depth_setter(0)
        self.algo = 'bfs'
        self.choices = {1:'download', 2:'error', 3:'search', 4:'crawl'}
        self.choice = self.choices[4] #the default is crawl
        self.output = ""
        self.seed = ""
        self.list_of_links = []
        self.NOT_LINK = [
        'data',
        '#',
        ]
        self.SCHEME_HTTP = "http"
        self.SCHEME_HTTPS = "https"
        self.SUPPORTED_SCHEMES = (self.SCHEME_HTTP, self.SCHEME_HTTPS)

    def option(self):
        """
        Gets user input to set various program options related to
        how the user would like to handle crawling a webpage.

        Ask for users option choices

        """
        choice = raw_input("Choose your option \n"
                           + "Download Resources = 1 \n"
                           + "Check for Errors = 2 \n"
                           + "Search for Query = 3 \n"
                           + "Crawl all links = 4  \n")


    def HTML_corrector(self,base,link):
        """
        Fixes the link passed in such that it becomes either a functioning link or is flagged as a broken link.

        String link

        returns String corrected link
        """
        #TODO implement the corrected link,, look at the original web crawler
        pass


    def download_resources(self,link,options = '-A', file_type=None):
        """
        Writes all resources matching the given file type from the page link to the file specified by destination.

        String option
        String link
        String fileType=None

        returns
        """

        link = raw_input("Website you would like to download: ")
        file_type = raw_input("Enter the extension you would like to download: ")
        more_request = raw_input('Do you want more, enter Y or N: ')

        while more_request.lower() == 'y':
            more_file_type = raw_input("Enter the next extension you would like to download: ")
            file_type+= "," + more_file_type
            print file_type
            more_request = raw_input('Do you want to enter more extensions? Enter Y or N:')

        if file_type:
            p = subprocess.call(["wget",options,file_type,link])

        else:
            p = subprocess.call(["wget",options,link])



    def exact_query(self,query,data):
        """
        Returns a list of all occurrences of a given query in the data provided.

        String query
        String data

        returns Query results
        """
        pass

    def similar_query(self, query, data, proximity):
        """
        Returns a list of all occurrences within a certain deviation of a givegit n query in the data provided.

        String query
        String data
        int proximity

        returns Query results
        """
        pass


    def whitespace_checker(self,character):
        """
        Returns whether the character passed in is certain types of whitespace.

        char character

        returns boolean, if there is whitespace True
        """
        pass


    def find_links(self,data,destination):
        """
        Finds all the links (<a></a> anchor tags on page) on a page

        BeautifulSoup data
        String destination

        returns List of Links
        """
        pass


    def check_errors(self,link,list_of_links):
        """
        Checks the all the links and reports the error message associated with
        all the links inputed

        String list
        List list_of_links

        returns List of Errors
        """
        pass


    def parse_data(self,link):
        """
        Returns Beautiful object for the link given, this will allow modules parse through pages data much faster

        String link

        """
        pass


    def query_search(self,query,data,choice):
        """

        Writes all resources matching the given file type from the page link to the file specified by destination.

        String query
        String data
        String choice   (from a dictionary choice)

        returns Query results
        """
        #TODO link the choices to the correct methods

        choice = raw_input("Choose your option \n"
                       + "Similar Search = 1 \n"
                       + "Exact Search = 2 \n")
        pass


    def depth_setter(self, depth):
        """
        Sets the default max depth variable for the web crawler

        int depth

        """
        self.depth = depth

    def website_structure(self,link,depth):
        """
        It provides a structured model of the website and other site the initial site is connect to. It displays
        a hierarchy that will show users how crawled link interact with each other.

        String link
        int depth

        returns A pretty print of Hierarchy
        """
        pass

    def is_link(self,url):
        """Return True if the url is not base 64 data or a local ref (#)"""
        for prefix in self.NOT_LINK:
            if url.startswith(prefix):
                return False
        return True


    def get_clean_url_split(self,url):
        """Returns a clean SplitResult with a scheme and a valid path

        :param url: The url to clean
        :rtype: A urlparse.SplitResult
        """
        if not url:
            raise ValueError('The URL must not be empty')
        split_result = urlparse.urlsplit(url)

        if not split_result.scheme:
            if split_result.netloc:
                url = self.SCHEME_HTTP + ":" + url
            else:
                url = self.SCHEME_HTTP + "://" + url
            split_result = urlparse.urlsplit(url)

        split_result = self.convert_iri_to_uri(split_result)

        return split_result


    def convert_iri_to_uri(self,url_split):
        """Attempts to convert potential IRI to URI.

        IRI may contain non-ascii characters.
        """
        new_parts = []
        for i, part in enumerate(url_split):
            if i == 1:
                # domain name
                new_parts.append(part.encode('idna').decode('ascii'))
            else:
                # other parts such as path or query string.
                new_parts.append(self.url_encode_non_ascii(part))
        return urlparse.SplitResult(*new_parts)


    def url_encode_non_ascii(self,url_part):
        """For each byte in url_part, if the byte is outside ascii range, quote the
        byte. UTF characters that take two bytes will be correctly converted using
        this technique.

        We do not quote the whole url part because it might contain already quoted
        characters, which would then be double-quoted.

        The url part is converted from utf-8 and then to utf-8, which might not
        always work if there is mixed or bad encoding.
        """
        return re.sub(
            b'[\x80-\xFF]',
            lambda match: quote(match.group(0)).encode("utf-8"),
            url_part.encode("utf-8")).decode("ascii")


    def get_absolute_url_split(self,url, base_url_split):
        """Returns a SplitResult containing the new URL.

        :param url: The url (relative or absolute).
        :param base_url_split: THe SplitResult of the base URL.
        :rtype: A SplitResult
        """
        new_url = urlparse.urljoin(base_url_split.geturl(), url)

        return self.get_clean_url_split(new_url)


if __name__ == '__main__':
    crawler = Web_Crawler()
    #crawler.option()
    #print crawler.HTML_corrector('http://www.canvasgroup.ca','link')

    #crawler.get_absolute_url_split(url, base_url_split)
    #base_url_split = crawler.get_clean_url_split('http://www.canvasgroup.ca')
    #print(crawler.get_absolute_url_split("about.html", base_url_split).geturl())

    crawler.download_resources('http://www.canvasgroup.ca','jpg,png')

   #crawler.get_absolute_url_split(url, base_url_split)
    base_url_split = crawler.get_clean_url_split('http://www.canvasgroup.ca')
    print(crawler.get_absolute_url_split("about.html", base_url_split).geturl())

