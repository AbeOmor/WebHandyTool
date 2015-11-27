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


def has_multiprocessing():
    has_multi = False

    try:
        import multiprocessing  # noqa
        has_multi = True
    except Exception:
        pass

    return has_multi


def has_gevent():
    has_gevent = False

    try:
        import gevent  # noqa
        has_gevent = True
    except Exception:
        pass

    return has_gevent

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
    def test_exact_string_search(self):
        searcher = search()
        inputString = ["Hello world!","","Hello. My name is Eric. I am writing this simple test to check to see how well my parsing algorithm is performing. hello again, dont forget my name: Eric. That is all."]
        queries = ['hello','LASDGLKGSVLIUGAEOUGSVLUHwe;ofrw.k?bwri;hqf.IBALIUGqleiugwKUGwrliugwrgOUGFW ;OURW;U','Eric','my name is Eric!','my name is Eric']
        self.assertEqual(
        [0],
        searcher.exact_query(queries[0],inputString[0]))


    def test_similar_string_search(self):
        searcher = search()



if __name__ == '__main__':
    urlTestSuite = unittest.TestLoader().loadTestsFromTestCase(urlCorrectorTest)
    unittest.TextTestRunner(verbosity=2).run(urlTestSuite)

    searchTestSuite = unittest.TestLoader().loadTestsFromTestCase(searchTest)
    unittest.TextTestRunner(verbosity=2).run(searchTestSuite)