import urllib2

import urlCorrector


class errors(object):

    def __init__(self):
        self.urlCorrect = urlCorrector.urlCorrector()

    def check_errors(self,link,list_of_links=None):
        """
        Checks the all the links and reports the error message associated with
        all the links inputted

        :param link:
        :param list_of_links:
        :return List of Errors:
        """

        status_msg_list = []
        base_url = self.urlCorrect.HTML_corrector(link)


        if list_of_links:
            for link in list_of_links:
                corrected_link = self.urlCorrect.absolute_HTML_corrector(link,base_url).geturl()
                request = urllib2.Request(corrected_link)

                try:
                   response = urllib2.urlopen(request)
                   success = 'Status code: ' + str(response.getcode())
                   print str(corrected_link) + ' -- ' + success
                   status_msg_list.append(str(corrected_link) + ' -- ' + success)

                except urllib2.HTTPError, e:
                   error = 'Error code: ' + str(e.code)
                   print str(corrected_link) + ' -- ' + error
                   status_msg_list.append(str(corrected_link) + ' -- ' + error)

            return status_msg_list

        else:
            base_url = base_url.geturl()
            request = urllib2.Request(base_url)
            try:
               response = urllib2.urlopen(request)
               success = 'Status code: ' + str(response.getcode())
               print str(base_url)  + ' -- ' + success

            except urllib2.HTTPError, e:
               error = 'Error code: ' + str(e.code)
               print str(base_url)  + ' -- ' + error

               return str(base_url) + ' -- ' + error

            return str(base_url) + ' -- ' + success