import subprocess
from bs4 import BeautifulSoup
from urllib2 import *
import datetime
import urllib2
import re

class urlCorrector(object):

    def __init__(self):
            self.list_of_links = []
            HTML_help = HTML_corrector_help()
            self.NOT_LINK = HTML_help.NOT_LINK
            self.SCHEME_HTTP = "http"
            self.SCHEME_HTTPS = "https"
            self.SUPPORTED_SCHEMES = (self.SCHEME_HTTP, self.SCHEME_HTTPS)

    def HTML_corrector(self,link):
        """
        Fixes the link passed in such that it becomes either a functioning link or is flagged as a broken link.
        :param link:
        :return  Url object of split url result corrected link Ex; SplitResult(scheme=u'http', netloc=u'canvasgroup.ca', path=u'/zdfzd', query=u'', fragment=u'') :
        """
        HTML_corrector_helper = HTML_corrector_help()
        if not link:
            raise ValueError('The URL must not be empty')
        split_result = urlparse.urlsplit(link)

        if not split_result.scheme:
            if split_result.netloc:
                url = self.SCHEME_HTTP + ":" + link
            else:
                url = self.SCHEME_HTTP + "://" + link
            split_result = urlparse.urlsplit(url)

        split_result = HTML_corrector_helper.convert_iri_to_uri(split_result)

        return split_result


    def absolute_HTML_corrector(self,link,base_link_split):
        """
        Takes in the base url and appends any relative or absolute links to the base urk.

        :param link:
        :param base_link_split:
        :return Url object of split url result corrected link Ex; SplitResult(scheme=u'http', netloc=u'canvasgroup.ca', path=u'/zdfzd', query=u'', fragment=u'') ::
        """
        new_link = urlparse.urljoin(base_link_split.geturl(), link)

        return self.HTML_corrector(new_link)

class HTML_corrector_help(object):
    """
    Library of helper functions that are used by HTML corrector to
    fix url links.
    """
    def __init__(self):
        self.NOT_LINK = ['data','#','mailto','tel', 'javascript']

    def is_link(self,url):
        """
        Return True if the url is not base 64 data or a local ref (#)

        :param url:
        :return Boolean either True or False:
        """

        for prefix in self.NOT_LINK:
            try:
                if url.startswith(prefix):
                    return False
            except AttributeError as e:
                pass
        return True

    def convert_iri_to_uri(self,url_split):
        """
        Attempts to convert potential IRI to URI.

        IRI may contain non-ascii characters.
        :param url_split:
        :return:
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
        """
        For each byte in url_part, if the byte is outside ascii range, quote the
        byte. UTF characters that take two bytes will be correctly converted using
        this technique.

        We do not quote the whole url part because it might contain already quoted
        characters, which would then be double-quoted.

        The url part is converted from utf-8 and then to utf-8, which might not
        always work if there is mixed or bad encoding.
        :param url_part:
        :return:
        """
        return re.sub(
            b'[\x80-\xFF]',
            lambda match: quote(match.group(0)).encode("utf-8"),
            url_part.encode("utf-8")).decode("ascii")