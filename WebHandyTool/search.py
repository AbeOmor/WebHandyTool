from urllib2 import *
from parsers import parsers
from config import getConfig
class search(object):

    def __init__(self):
        self.list_of_links = []
        self.SCHEME_HTTP = "http"
        self.SCHEME_HTTPS = "https"
        self.SUPPORTED_SCHEMES = (self.SCHEME_HTTP, self.SCHEME_HTTPS)
        self.parser = parsers()
        self.search_choices = {'1':'exact', '2':'similar'}
        config = getConfig()
        self.search_choice= config["string_search"]["type"]
        self.setProximity(config["string_search"]["proximity"])

    def query_search(self,query,link,list_of_links = None,choice='exact'):
        """
        Find queries

        :param query:
        :param data:
        :param choice:
        :return Query results:
        """
        if list_of_links:
            print 'Links searching...'
            print list_of_links
            for link in list_of_links:
                data = self.parser.HTML_text(link)
                if choice == "exact":
                    print 'Hey Buddy...I just searched ' + str(link)
                    indexes = self.exact_query(query,data)
                    print indexes
                    for index in indexes :
                        print 'Found at index ' + str(index)
                        print '---------------------------------------------'
                        print data[index-30:index+30]
                        print '---------------------------------------------'

                elif choice == "similar":
                    print 'Hey Buddy...I just searched ' + str(link)
                    indexes = self.similar_query(query,data,self.proximity)
                    print indexes
                    for index in indexes:
                        print 'Found at index ' + str(index)
                        print '---------------------------------------------'
                        print data[index-30:index+30]
                        print '---------------------------------------------'
        else:
            data = self.parser.HTML_text(link)
            if choice == "exact":
                indexes = self.exact_query(query,data)
                print indexes
                for index in indexes :
                    print 'Found at index ' + str(index)
                    print '---------------------------------------------'
                    print data[index-30:index+30]
                    print '---------------------------------------------'

            elif choice == "similar":
                indexes = self.similar_query(query,data,self.proximity)
                print indexes
                for index in indexes:
                    print 'Found at index ' + str(index)
                    print '---------------------------------------------'
                    print data[index-30:index+30]
                    print '---------------------------------------------'

        return indexes

    def exact_query(self,query,data):
        """
        Searches through a String for a certain phrase or term. Returns the starting index for all occurrences of the query String.
        If the query is not located, it will return an empty array.

        :param query - The String we are looking for:
        :param data - The String we are searching through.:
        :return Indexes corresponding to the beginning of the location of the String in question.:
        """
        locations = [];
        queryIndex = 0;

        data.strip();
        query.strip();
        query = query.lower();
        data = data.lower();
                                                    # Impossible for data to contain query or query is nonsensical.
        if len(query) > len(data) or (len(query) == len(data) and not query is data) or len(query) == 0:
            return [];

        for i in range(0, len(data)):
            if data[i] == query[queryIndex]:        # Current location is matching the query pattern so far.
                if queryIndex == len(query) - 1:    # The whole query pattern is matched, add starting index.
                    locations.append(i - len(query) + 1);
                    queryIndex = 0;
                else:
                    queryIndex += 1;

            else:                                   #Current location didn't match the pattern.
                if data[i] == query[0]:
                    queryIndex = 1;
                else:
                    queryIndex = 0;

        return locations;

    def similar_query(self, query, data, proximity):
        """
        Searches through a String for a certain phrase or term. Returns results that are close to the query as well.
        (i.e. "ap ple" or "bpple" would be noted for "apple") Returns the starting index for all occurrences of Strings sufficiently close to
        the query. If the query is not located, it will return an empty array.

        :param: query  - The String we are looking for.
        :param: data - The String we are searching through.:
        :param: proximity - The size of the acceptable variation from the query.:
        :return:Indexes corresponding to the beginning of the location of the String in question.
        """
        locations = [];
        queryIndex = 0;
        distance = 0;

        data.strip();
        query.strip();
        query = query.lower();
        data = data.lower();
        if len(query) > len(data) or (len(query) == len(data) and not query is data) or len(query) == 0 or proximity > (0.4) * len(query):
            return [];

        for i in range(0, len(data)):
            if data[i] == query[queryIndex]:
                if queryIndex == len(query) - 1:
                    locations.append(i - len(query) + 1);
                    queryIndex = 0;
                    distance = 0;
                else:
                    queryIndex += 1;
            elif distance < proximity:
                if queryIndex == len(query) - 1:
                    locations.append(i - len(query) + 1);
                    queryIndex = 0;
                    distance = 0;
                elif self.whitespace_checker(data[i]):
                    distance += 1;
                else:
                    distance += 1;
                    queryIndex += 1;
            else:
                if data[i] == query[0]:
                    queryIndex = 1;
                    distance = 0;
                else:
                    queryIndex = 0;
                    distance = 0;

        return locations;

    def whitespace_checker(self,character):
        """
        Returns true if the character passed in is a whitespace character such as tab, space or newline.

        :param character - The character to be checked.:
        :return boolean, if there is whitespace True,Whether the character is whitespace:
        """
        return character == ' ' or character == '    ' or character == os.linesep;

    def setProximity(self,proximity):
        """
        Set the search proximity
        :param proximity:
        :return:
        """
        self.proximity = proximity;
