"""
Unit and integration tests for WebHandyTool
"""
import os
import logging
import sys
from tempfile import mkstemp
import time
import threading
import unittest


from urlCorrector import *
from linkSearchAlgos import linkSearchAlgos
from download import download
from errors import errors
from parsers import parsers
from search import search

import SocketServer, SimpleHTTPServer

TEST_FILES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                              'testfiles')

# UTILITY CLASSES AND FUNCTIONS ###

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


def start_http_server():
    """Starts a simple http server for the test files"""
    # For the http handler
    os.chdir(TEST_FILES_DIR)
    handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    handler.extensions_map['.html'] = 'text/html; charset=UTF-8'
    httpd = ThreadedTCPServer(("localhost", 0), handler)
    ip, port = httpd.server_address

    httpd_thread = threading.Thread(target=httpd.serve_forever)
    httpd_thread.setDaemon(True)
    httpd_thread.start()

    return (ip, port, httpd, httpd_thread)

class urlCorrectorTest(unittest.TestCase):
    def test_clean_url_split(self):
        urlCorrect = urlCorrector()
        self.assertEqual(
            "http://www.example.com",
            urlCorrect.HTML_corrector("www.example.com").geturl())
        self.assertEqual(
            "http://www.example.com",
            urlCorrect.HTML_corrector("//www.example.com").geturl())
        self.assertEqual(
            "http://www.example.com",
            urlCorrect.HTML_corrector("http://www.example.com").geturl())

        self.assertEqual(
            "http://www.example.com/",
            urlCorrect.HTML_corrector("www.example.com/").geturl())
        self.assertEqual(
            "http://www.example.com/",
            urlCorrect.HTML_corrector("//www.example.com/").geturl())
        self.assertEqual(
            "http://www.example.com/",
            urlCorrect.HTML_corrector("http://www.example.com/").geturl())

    def test_get_absolute_url(self):
        urlCorrect = urlCorrector()
        base_url_split = urlCorrect.HTML_corrector(
            "https://www.example.com/hello/index.html")
        self.assertEqual(
            "https://www.example2.com/test.js",
            urlCorrect.absolute_HTML_corrector(
                "//www.example2.com/test.js", base_url_split).geturl())
        self.assertEqual(
            "https://www.example.com/hello2/test.html",
            urlCorrect.absolute_HTML_corrector(
                "/hello2/test.html", base_url_split).geturl())
        self.assertEqual(
            "https://www.example.com/hello/test.html",
            urlCorrect.absolute_HTML_corrector("test.html", base_url_split).geturl())
        self.assertEqual(
            "https://www.example.com/test.html",
            urlCorrect.absolute_HTML_corrector("../test.html", base_url_split).geturl())

class searchTest(unittest.TestCase):
    def test_exact_string_search_1(self):
        searcher = search()
        inputString = "Hello world!"
        queries = ['hello','LASDGLKGSVLIUGAEOUGSVLUHwe;ofrw.k?bwri;hqf.IBALIUGqleiugwKUGwrliugwrgOUGFW ;OURW;U','Eric','my name is Eric!','my name is Eric']
        self.assertEqual(
        [0],
        searcher.exact_query(queries[0],inputString))
        self.assertEqual(
        [],
        searcher.exact_query(queries[1],inputString))
        self.assertEqual(
        [],
        searcher.exact_query(queries[2],inputString))
        self.assertEqual(
        [],
        searcher.exact_query(queries[3],inputString))
        self.assertEqual(
        [],
        searcher.exact_query(queries[4],inputString))

    def test_exact_string_search_2(self):
        searcher = search()
        inputString = ""
        queries = ['hello','LASDGLKGSVLIUGAEOUGSVLUHwe;ofrw.k?bwri;hqf.IBALIUGqleiugwKUGwrliugwrgOUGFW ;OURW;U','Eric','my name is Eric!','my name is Eric']
        self.assertEqual(
        [],
        searcher.exact_query(queries[0],inputString))
        self.assertEqual(
        [],
        searcher.exact_query(queries[1],inputString))
        self.assertEqual(
        [],
        searcher.exact_query(queries[2],inputString))
        self.assertEqual(
        [],
        searcher.exact_query(queries[3],inputString))
        self.assertEqual(
        [],
        searcher.exact_query(queries[4],inputString))

    def test_exact_string_search_3(self):
        searcher = search()
        inputString = "Hello. My name is Eric. I am writing this simple test to check to see how well my parsing algorithm is performing. hello again, dont forget my name: Eric. That is all."
        queries = ['hello','LASDGLKGSVLIUGAEOUGSVLUHwe;ofrw.k?bwri;hqf.IBALIUGqleiugwKUGwrliugwrgOUGFW ;OURW;U','Eric','my name is Eric!','my name is Eric']
        self.assertEqual(
        [0,115],
        searcher.exact_query(queries[0],inputString))
        self.assertEqual(
        [],
        searcher.exact_query(queries[1],inputString))
        self.assertEqual(
        [18,149],
        searcher.exact_query(queries[2],inputString))
        self.assertEqual(
        [],
        searcher.exact_query(queries[3],inputString))
        self.assertEqual(
        [7],
        searcher.exact_query(queries[4],inputString))


    def test_similar_string_search_1(self):
        searcher = search()
        inputString = "Here comes my hero"
        queries = 'HERE'
        self.assertEqual(
        [0,14],
        searcher.similar_query(queries,inputString,1))

    def test_similar_string_search_2(self):
        searcher = search()
        inputString = "Some text, hello"
        queries = 'hello'
        self.assertEqual(
        [11],
        searcher.similar_query(queries,inputString,2))

    def test_similar_string_search_3(self):
        searcher = search()
        inputString = "hehhhehellp"
        queries = 'hello'
        self.assertEqual(
        [6],
        searcher.similar_query(queries,inputString,1))

    def test_similar_string_search_4(self):
        searcher = search()
        inputString = ". \n .. \n q1/.SQL \n q2.SQL \n fileResult.txt"
        queries = 'fileResults'
        self.assertEqual(
        [28],
        searcher.similar_query(queries,inputString,1))

    def test_similar_string_search_5(self):
        searcher = search()
        inputString = ". \n .. \n q1/.SQL \n q2.SQL \n fileResult.txt"
        queries = 'fileResults'
        self.assertEqual(
        [28],
        searcher.similar_query(queries,inputString,1))

class crawlerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        (cls.ip, cls.port, cls.httpd, cls.httpd_thread) = start_http_server()

        # FIXME replace by thread synchronization on start
        time.sleep(0.2)

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()

    def setUp(self):
        # We must do this because Python 2.6 does not have setUpClass
        # This will only be executed if setUpClass is ignored.
        # It will not be shutdown properly though, but this does not prevent
        # the unit test to run properly
        if not hasattr(self, 'port'):
            (self.ip, self.port, self.httpd, self.httpd_thread) =\
                start_http_server()
            # FIXME replace by thread synchronization on start
            time.sleep(0.2)

    def get_url(self, test_url):
        return "http://{0}:{1}{2}".format(self.ip, self.port, test_url)


    def get_url_open(self):
        # Not automatically imported to allow monkey patching.
        if sys.version_info[0] < 3:
            from urllib2 import urlopen
        else:
            from urllib.request import urlopen
        return urlopen


    def get_url_request(self):
        if sys.version_info[0] < 3:
            from urllib2 import Request
        else:
            from urllib.request import Request
        return Request

    def test_404_error(self):
        errorCheck = errors()
        urlopen = self.get_url_open()
        url = self.get_url("/does_not_exist.html")
        response = errorCheck.check_errors(url)

        self.assertEqual(url +" -- Error code: 404", response)

    def test_200_error(self):
        errorCheck = errors()
        urlopen = self.get_url_open()
        url = self.get_url("/index.html")
        response = errorCheck.check_errors(url)

        self.assertEqual(url +" -- Status code: 200", response)

    def test_link_grabber(self):
        urlopen = self.get_url_open()
        url = self.get_url("/index.html")
        linkSearch = linkSearchAlgos()
        links = linkSearch.find_links(url)
        self.assertEqual([None, u'a.html', u'sub/b.html', u'/c.html', u'd.html', u'//www.perdu.com'], links)

    def test_BFS_depth_0(self):
        url = self.get_url("/depth/root.html")
        urlopen = self.get_url_open()
        linkSearch = linkSearchAlgos()
        linkSearch.depth_setter(0)
        links = linkSearch.bfs(url)
        expected_link = [u'root.html']
        i=0
        for link in links:
            self.assertTrue(expected_link[i] in link)
            i = i+1

    def test_BFS_depth_1(self):
        url = self.get_url("/depth/root.html")
        urlopen = self.get_url_open()
        linkSearch = linkSearchAlgos()
        linkSearch.depth_setter(1)
        links = linkSearch.bfs(url)
        expected_link = [u'/root.html', u'/0.html']
        i=0
        for link in links:
            self.assertTrue(expected_link[i] in link)
            i = i+1

    def test_BFS_depth_2(self):
        url = self.get_url("/depth/root.html")
        urlopen = self.get_url_open()
        linkSearch = linkSearchAlgos()
        linkSearch.depth_setter(2)
        links = linkSearch.bfs(url)
        expected_link = [u'/root.html', u'/0.html', u'/1.html']
        i=0
        for link in links:
            self.assertTrue(expected_link[i] in link)
            i = i+1

    def test_BFS_depth_3(self):
        url = self.get_url("/depth/root.html")
        urlopen = self.get_url_open()
        linkSearch = linkSearchAlgos()
        linkSearch.depth_setter(3)
        links = linkSearch.bfs(url)
        expected_link = [u'/root.html', u'/0.html', u'/1.html', u'/2.html']
        i=0
        for link in links:
            self.assertTrue(expected_link[i] in link)
            i = i+1

    def test_BFS_depth_4(self):
        url = self.get_url("/depth/root.html")
        urlopen = self.get_url_open()
        linkSearch = linkSearchAlgos()
        linkSearch.depth_setter(4)
        links = linkSearch.bfs(url)
        expected_link = [u'/root.html', u'/0.html', u'/1.html', u'/2.html', u'/3.html']
        i=0
        for link in links:
            self.assertTrue(expected_link[i] in link)
            i = i+1

    def test_BFS_depth_5(self):
        url = self.get_url("/depth/root.html")
        urlopen = self.get_url_open()
        linkSearch = linkSearchAlgos()
        linkSearch.depth_setter(5)
        links = linkSearch.bfs(url)
        expected_link = [u'/root.html', u'/0.html', u'/1.html', u'/2.html', u'/3.html', u'/4.html']
        i=0
        for link in links:
            self.assertTrue(expected_link[i] in link)
            i = i+1


    def test_download(self):
        url = self.get_url("/sub")
        urlopen = self.get_url_open()
        downloading = download()
        downloading.download_resources(url,'*.js')

if __name__ == '__main__':

    #Test the urlCorrector
    urlTestSuite = unittest.TestLoader().loadTestsFromTestCase(urlCorrectorTest)
    unittest.TextTestRunner(verbosity=2).run(urlTestSuite)

    #Test the search string algorithm
    searchTestSuite = unittest.TestLoader().loadTestsFromTestCase(searchTest)
    unittest.TextTestRunner(verbosity=2).run(searchTestSuite)

    #Test the crawlers functions and bfs
    crawlTestSuite = unittest.TestLoader().loadTestsFromTestCase(crawlerTest)
    unittest.TextTestRunner(verbosity=2).run(crawlTestSuite)
    print "Manual Check is test.js was downloaded in a 127.0.0.1:* directory in the testfiles directory"