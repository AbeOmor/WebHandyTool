__author__ = 'Abe'

"""
Main class, it is for crawling.
Class variable includes depth,algo,chocies,choice,output,seed,list of links
"""
class Web_Crawler(object):
    def __init__(self):
        self.depth = self.depth_setter(0)
        self.algo = 'bfs'
        self.choices = {1:'download', 2:'error', 3:'search', 4:'crawl'}
        self.choice = self.choices[4] #the default is crawl
        self.output = ""
        self.seed = ""
        self.list_of_links = []

    """
    Gets user input to set various program options related to
    how the user would like to handle crawling a webpage.

    Ask for users option choices

    """
    def option(self):
        choice = raw_input("Choose your option \n"
                           + "Download Resources = 1 \n"
                           + "Check for Errors = 2 \n"
                           + "Search for Query = 3 \n"
                           + "Crawl all links = 4  \n")

    """
    Fixes the link passed in such that it becomes either a functioning link or is flagged as a broken link.

    String link

    returns String corrected link
    """
    def HTML_corrector(self,link):
        #TODO implement the corrected link,, look at the original web crawler
        corrected_link = link
        return corrected_link

    """
    Writes all resources matching the given file type from the page link to the file specified by destination.

    String link
    String fileType
    String destination

    """
    def download_resources(self,link,fileType,destination):
        destination = self.output
        pass

    """
    Returns a list of all occurrences of a given query in the data provided.

    String query
    String data

    returns Query results
    """
    def exact_query(self,query,data):
        pass

    """
    Returns a list of all occurrences within a certain deviation of a givegit n query in the data provided.

    String query
    String data
    int proximity

    returns Query results
    """
    def similar_query(self, query, data, proximity):
        pass

    """
    Returns whether the character passed in is certain types of whitespace.

    char character

    returns boolean, if there is whitespace True
    """
    def whitespace_checker(self,character):
        pass

    """
    Finds all the links (<a></a> anchor tags on page) on a page

    BeautifulSoup data
    String destination

    returns List of Links
    """
    def find_links(self,data,destination):
        pass

    """
    Checks the all the links and reports the error message associated with
    all the links inputed

    String list
    List list_of_links

    returns List of Errors
    """
    def check_errors(self,link,list_of_links):
        pass

    """
    Returns Beautiful object for the link given, this will allow modules parse through pages data much faster

    String link

    """
    def parse_data(self,link):
        pass

    """

    Writes all resources matching the given file type from the page link to the file specified by destination.

    String query
    String data
    String choice   (from a dictionary choice)

    returns Query results
    """
    def query_search(self,query,data,choice):
        #TODO link the choices to the correct methods

        choice = raw_input("Choose your option \n"
                       + "Similar Search = 1 \n"
                       + "Exact Search = 2 \n")
        pass

    """
    Sets the default max depth variable for the web crawler

    int depth

    """
    def depth_setter(self, depth):
        self.depth = depth

    """
    It provides a structured model of the website and other site the initial site is connect to. It displays
    a hierarchy that will show users how crawled link interact with each other.

    String link
    int depth

    returns A pretty print of Hierarchy
    """
    def website_structure(self,link,depth):
        pass

if __name__ == '__main__':
    crawler = Web_Crawler()
    crawler.option()

