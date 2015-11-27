__author__ = 'Abe'
import subprocess
import datetime

from urlCorrector import *
from linkSearchAlgos import linkSearchAlgos
from download import download
from errors import errors
from parsers import parsers
from search import search

class Web_Crawler(object):
    """
    Main class, it is for crawling.
    Class variable includes depth,algo,choices,choice,output,seed,list of links
    """
    def __init__(self):
        self.urlCorrect = urlCorrector()
        self.HTML_corrector_helper = HTML_corrector_help()
        self.download = download()
        self.errors = errors()
        self.parsers = parsers()
        self.choices = {'1':'download', '2':'error', '3':'search', '4':'crawl','5':'web structure'}
        self.choice = self.choices['4'] #the default is crawl
        self.list_of_links = self.urlCorrect.list_of_links
        self.NOT_LINK = self.urlCorrect.NOT_LINK
        self.SCHEME_HTTP = self.urlCorrect.SCHEME_HTTP
        self.SCHEME_HTTPS = self.urlCorrect.SCHEME_HTTPS
        self.SUPPORTED_SCHEMES = self.urlCorrect.SUPPORTED_SCHEMES

    def option(self):
        """
        Gets user input to set various program options related to
        how the user would like to handle crawling a webpage.

        Ask for users option choices

        :return:
        """
        choice = raw_input("Choose your option \n"
                           + "Download Resources = 1 \n"
                           + "Check for Errors = 2 \n"
                           + "Search for Query = 3 \n"
                           + "Just Crawl = 4  \n")

        self.choice = self.choices.get(choice)

        link = raw_input("Website you would like use: ")
        link = self.urlCorrect.HTML_corrector(link).geturl()

        #parseType = raw_input("Would you like to do a breadth-first (0) or depth-first (1) search?");
        self.choice = self.choices.get(choice)

        if self.choice == "download":
            self.download.download_resources(link)

        elif self.choice == "error":
            self.algo = linkSearchAlgos()
            self.list_of_links = self.algo.bfs(link)
            self.errors.check_errors(link,self.list_of_links)

        elif self.choice == "search":
            self.algo = linkSearchAlgos()
            searchOp = search()
            query = raw_input("What's your query: ")
            searchOp.search_choice = searchOp.search_choices.get(searchOp.search_choice)
            list_of_links = self.algo.bfs(link)

            searchOp.query_search(query,link,list_of_links,searchOp.search_choice)

        elif self.choice == "crawl":
            self.algo = linkSearchAlgos()
            self.list_of_links = self.algo.bfs(link)
            print "THE LINK ON SELECTED DEPTH"
            print self.list_of_links

        else:
            print "Incorrect input."


if __name__ == '__main__':
    crawler = Web_Crawler()
    option = crawler.option()

