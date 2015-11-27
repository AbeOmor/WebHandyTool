import subprocess
from config import getConfig

class download(object):
    def __init__(self):
        self.config = getConfig()

    def download_resources(self,link, file_type=None):
        """
        Writes all resources matching the given file type from the page link to the file specified by destination.

        :param link:
        :param options:
        :param file_type:
        :return:
        """
        if not file_type:
            file_type = self.config["download"]["file_types"]

        options = self.config["download"]["option"]

        if file_type:
            # Call UNIX wget process to download files
            p = subprocess.call(["wget",options,file_type,link])
        else:
            p = subprocess.call(["wget",options,link])