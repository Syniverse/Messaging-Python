"""
Syniverse Messaging API

This module provides easy access to the Syniverse Messaging API.
"""

import json
import logging
import time
import json

try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client

import six
import requests



###--- TMP code to have visuality into the request module
# http_client.HTTPConnection.debuglevel = 1
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

class ScgapiException(Exception):
    """Base exception for exceptions used by the SDK."""
    pass

class HttpRequestError(ScgapiException):
    """A HTTP request failed."""
    pass

class ApiCallFailedError(ScgapiException):
    """An API returned an error. One or more operations failed."""
    pass

class ImmutableObjectError(ScgapiException):
    """An API returned an error. One or more operations failed."""
    pass

class AuthenticationError(ScgapiException):
    """Failed to autnenticate with server"""
    pass


def to_ansi_date(val):
    return time.strftime('%Y-%m-%d', time.localtime(int(val)/1000))


_logger = None

class Log(object):
    """ Internal logger"""
    @staticmethod
    def debug(message):
        """Log debug message"""
        global _logger
        if _logger is not None:
            _logger.debug(message)

    @staticmethod
    def error(message):
        """Log error message"""
        global _logger
        if _logger is not None:
            _logger.error(message)

    @staticmethod
    def info(message):
        """Log info message"""
        global _logger
        if _logger is not None:
            _logger.info(message)

    @staticmethod
    def get_logger():
        """Get the logger for this module."""
        global _logger
        if _logger is None:
            _logger = logging.getLogger("scgapi")
            handler = logging.FileHandler("scgapi.log")
            _logger.addHandler(handler)
        return _logger

def init_from_json(data, cls, resource=None):
    for k in cls._get_member_variable_names():
        if k.startswith("_"):
            setattr(cls, k, data.get(k[1:], None))
        else:
            setattr(cls, k, data.get(k, None))
    if resource is not None:
        cls.set_resource(resource)
    return cls

def add_list_from_json(data, key, factory):
    data_list = data.get(key, None)
    if data_list:
        obj = []
        for item in data_list:
            obj.append(factory(item))
        return obj
    return None

def to_dict(obj, keys=None):
    attributes = {}
    if not keys:
        keys = vars(obj).keys()
    for k in keys:
        if not k.startswith("_"):
            attributes[k] = getattr(obj, k)

    return attributes

class ObjBase(object):
    def __init__(self):
        self.__resource = None

    def __eq__(self, other):
        try:
            for name in self._get_member_variable_names():
                if getattr(self, name) != getattr(other, name):
                    return False
        except Exception:
            return False
        else:
            return True

    def to_dict(self):
        return to_dict(self, self._get_member_variable_names())

    def _locals(self):
        """Like locals(self), but with only actual attributes that has values"""

        locals_ = {}
        for name in self._get_member_variable_names():
            value = getattr(self, name, None)
            if value is not None:
                locals_[name] = value
        return locals_

    def _init(self, **kwargs):
        attributes = self._get_member_variable_names()

        for name in attributes:
            if not name in kwargs:
                #print("Setting %s --> None" % name)
                try:
                    setattr(self, name, None)
                except:
                    print("Failed setting %s --> None" % name)
                    raise

        for key, value in kwargs.items():
            if not key in attributes:
                raise AttributeError(key)
            #print("Setting %s --> %s " % key % value)
            setattr(self, key, value)

    def wash_args(self, **kwargs):
        if kwargs and len(kwargs) == 1:
            instance_value = six.next(six.itervalues(kwargs))
            if isinstance(instance_value, type(self)):
                return instance_value._locals()

        args = {}
        allowed = self._get_member_variable_names()
        for k, v in kwargs.items():
            if k.endswith("_"):
                key = k[:-1]
            else:
                key = k
            if not key in allowed:
                #print("Invalid key" , key)
                raise AttributeError(k)
            if v:
                args[key] = v
        return args

    def _get_member_variable_names(self):
        pass # Override

    def _delete(self):
        self.get_resource().delete(self._id)

    def _update(self):
        self.get_resource().update(self)

    def get_session(self):
        return self.get_resource()._session

    def set_resource(self, resource):
        self.__resource = resource

    def get_resource(self):
        return self.__resource


class ListParameters:

    def __init__(self):
        self.start_offset = None
        self.page_size = None # use default
        self.sort = None


class ResourceBase(object):

    def __init__(self, session, url_path, cls):
        self._session = session
        self._url_path = url_path
        self._cls = cls


    def _list(self, **kwargs):
        """
        Get the object(s) matching the filter.

        A ListParameters class may be added to the list of
        arguments as "list_parameters=...".

        :return: Generator that provides object instances
        """

        offset = 0

        lp = None
        if "list_parameters" in kwargs:
            lp = kwargs["list_parameters"]
            del kwargs["list_parameters"]

        attributes = self._cls().wash_args(**kwargs)
        if lp is not None:
            if lp.start_offset is not None:
                attributes = lp.start_offest
            if lp.page_size is not None:
                attributes["limit"] = lp.page_size
            if lp.sort is not None:
                attributes["sort"] = lp.sort

        return self._session._iterate_over(
            lambda offset: self._session._get_request(
                self._url_path,
                attributes,
                offset=offset),
            lambda json: self._cls._create_from_json(json, self),
            offset)


    def _get(self, id):
        """
        Get an instance of an object

        :param id: Id of the object

        :returns: Instance of an object.
        """

        return self._cls._create_from_json(
            self._session._get_request(self._url_path, {}, id=id), self)


    def _create(self, **kwargs):
        """
        Create an object

        :return: The unique id of the new object.
        """

        rval = self._session._post_request(
            self._url_path,
            self._cls().wash_args(**kwargs))
        return rval["id"]

    def _update(self, obj):
        """
        Update an object

        :param obj: An instance of the object to update.

        :return: True if the operation was successful.
        """

        data = obj.to_dict()

        if hasattr(obj, "_version_number"):
            data["version_number"] = obj._version_number

        return self._session._post_update_request(self._url_path, data, obj._id)

    def _delete(self, obj):
        """
        Delete an object

        :param obj: An instance of the object to delete, or a string with the unique object id.

        :return: True if the operation was successful.
        """

        if isinstance(obj, self._cls):
            id = obj._id
        else:
            id = obj # assume string
        return self._session._delete_request(self._url_path, id)


class ResourceImpl(ResourceBase):

    def __init__(self, session, url_path, cls):
        super(ResourceImpl, self).__init__(session, url_path, cls)

    def list(self, **kwargs):
        return self._list(**kwargs)

    def get(self, id):
        return self._get(id)

    def create(self, **kwargs):
        return self._create(**kwargs)

    def update(self, obj):
        return self._update(obj)

    def delete(self, obj):
        return self._delete(obj)

class AuthInfo:
    """Authentication data for the API server"""
    def __init__(self, key=None, secret=None, token=None, config=None):
        """Constructor

        Args:
            key (str): Your key
            secret (str): Your secret
            token (str): Your current token
            config (str): If used, this loads the configuration from a json file
                with the name provided in this argument. The other arguments
                are not used.

        Examples:
            auth = scgapi.AuthInfo("<Consumer key>",
                    "<Consumer secret>",
                    "<Access token>")

            auth = scgapi.AuthInfo(config="auth.json")
        """
        self.key = key
        self.secret = secret
        self.token = token
        self.retries = 3
        if config is not None:
            self.load_json(config)
        elif key == None:
            # For testing of the SDK by the SDK developers
            self.appid = 0
            self.companyid = 0

    def _get_member_variable_names(self):
        return ("key", "secret", "token", "appid", "companyid", "quotaplan")

    def load_json(self, path):
        """Load config from a json file"""
        with open(path, 'r') as myfile:
            data = myfile.read()
        json_data = json.loads(data)
        init_from_json(json_data, self)
        return self
