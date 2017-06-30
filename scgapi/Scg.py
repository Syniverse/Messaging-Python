"""
SCG entry point object

This object initialize the SCG SDK, defines logging options and
gives acts as a factory for Session instances.
"""

import logging
import scgapi
from scgapi.Session import Session

class Scg(object):
    """
    Entry point to the SCG API

    This class allows you to connect to an SCG API server
    """

    def __init__(self, log=False, log_level=None):
        """
        Constructor

        :param log True to enable logging
        :param log_level Log level to use. Default is logging.INFO
        """

        self.logger = scgapi.Log.get_logger() if log else None
        effective_log_level = log_level if log_level else logging.INFO
        if self.logger:
            self.logger.setLevel(effective_log_level)

    def connect(self, auth, url=None):
        """
        Establish a connection to the API server

        :returns: Instance of Session
        """
        if url is None:
            url = 'https://api.syniverse.com'
        return Session(self, url, auth)

