"""
Session to the SCG API server.

A Session instance provides synchronous access to the SCG API
server. This class is designed to be used used by higher level objects
in this SDK.

If the API key expires during a session, the Session object will attempt
to acquire a new API key transparently to the user of the SDK.
"""

import scgapi
import requests
import json
import os
#import collections

class Session(object):
    """
    Session with the SCG API server

    All requests will raise an exception if the request was
    unsuccessful.
    """

    def __init__(self, parent, base_url, auth, api_url="/scg-external-api/api/v1"):
        self._parent = parent
        self._auth = auth;
        self._base_url = base_url
        self._api_url = api_url
        self._session = requests.Session()
        self._iterations = 0
        self._session.headers = {"Accept" : "*/*"}
        self.__set_auth_token()

    def __set_auth_token(self):
        if self._auth.token == None:
            self._session.headers["int-appId"] =  self._auth.appid
            self._session.headers["int-companyId"] = self._auth.companyid
            self._session.headers["int-txnId"] = "bogus-transaction-id"
            self._session.headers["int-quota-plan"] = self._auth.quotaplan
        else:
            self._session.headers["Authorization"] = "Bearer " + self._auth.token

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def _reset_auth(self):
        url = "https://api.syniverse.com/saop-rest-data/v1/apptoken-refresh"
        res = self._session.get(url,
                                 params={"consumerkey":self._auth.key,
                                         "consumersecret": self._auth.secret,
                                         "oldtoken": self._auth.token})
        if res.status_code == 200:
            json = res.json()
            self._auth.token = json["accessToken"]
            self.__set_auth_token()
        else:
            raise scgapi.AuthenticationError()

    def __unfold_dict_or_var(self, unknown):
        if hasattr(unknown, "to_dict"):
            return unknown.to_dict()
        return unknown

    def _get_params(self, params):
        nep = {}
        for k, v in params.items():
            if v != None and k != "self":
                if isinstance(v, list) or isinstance(v, tuple):
                    tmp_v = []
                    for vv in v:
                        tmp_v.append(self.__unfold_dict_or_var(vv))
                    nep[k] = tmp_v
                else:
                    nep[k] = self.__unfold_dict_or_var(v)
        return nep

    def _get_real_url(self, path, id=None, api_url=None):

        if api_url is None:
            api_url = self._api_url

        if id:
            return self._base_url + api_url + path + "/" + id
        return self._base_url + api_url + path


    def _send_request(self, req, ok_codes=[200, 204], recurse=0):
        try:
            result = req()
        except Exception as ex:
            scgapi.Log.error("Request failed: %s" % ex)
            raise scgapi.HttpRequestError(ex)
        else:
            if result.status_code == 401:
                if recurse < self._auth.retries:
                    self._reset_auth();
                    return self._send_request(req, ok_codes, recurse + 1)
            if not result.status_code in ok_codes:
                scgapi.Log.error(
                    "Request failed with HTTP status: %d %s"
                    % (result.status_code, result.reason))
                raise scgapi.HttpRequestError(
                    "HTTP error: %i %s" % (result.status_code, result.reason))

        return result


    def _get_request(self, path, params, offset=None, id=None):
        real_url = self._get_real_url(path, id)

        scgapi.Log.debug(
            "Request: GET '" + real_url + "', Args: %s" % params)

        if params is not None:
            use_params = self._get_params(params)
        else:
            use_params = {}

        if offset:
            use_params["offset"] = offset

        result = self._send_request(
            lambda: self._session.get(real_url, params=use_params))
        if result is not None:
            json_data = result.json()
            scgapi.Log.debug("Request: GET '" + real_url
                         + "', incoming Json: %s" % json_data)

            return json_data
        return None


    def _post_request(self, path, params, id=None, json_result=True, use_url_directly=False):

        if use_url_directly:
            real_url = path
        else:
            real_url = self._get_real_url(path, id)

        json_data = json.dumps(self._get_params(params))
        scgapi.Log.debug("Request: POST '" + real_url
                         + "', Json: %s" % json_data)
        result = self._send_request(
            lambda: self._session.post(
                real_url, data=json_data,
                headers={"Content-Type" : "Application/json"}))

        if json_result and result.status_code != 204:
            return result.json()

        return None


    def _post_file(self, path, file_path, api_url=None):
        real_url = self._get_real_url(path, api_url=api_url)
        with open(file_path, "rb") as file:
            scgapi.Log.debug("Request: POST '" + real_url
                             + " --> Upload: '" + file_path + "' "
                             + str(os.path.getsize(file_path)) + " bytes")
            result = self._send_request(
            lambda: self._session.post(
                real_url, data=file,
                headers={"Content-Type" : "Application/octet-stream"}))


    def _get_file(self, path, file_path, api_url=None):
        real_url = self._get_real_url(path, api_url=api_url)
        with open(file_path, "wb") as file:
            if os.path.isfile(path):
                raise RuntimeError("The file: '" + path + "' already exists")
            scgapi.Log.debug("Request: GET '" + real_url
                             + " --> Download: '" + file_path + "'")
            result = self._send_request(
                lambda: self._session.get(
                    real_url, stream=True,
                    headers={"Accept" : "Application/octet-stream"}))
            chunk_size = 1024
            for chunk in result.iter_content(chunk_size):
                file.write(chunk)


    def _post_update_request(self, path, obj_dict, id):
        real_url = self._get_real_url(path, id=id)

        json_dict = self._get_params(obj_dict)
        json_data = json.dumps(json_dict)

        scgapi.Log.debug("Request: POST '" + real_url
                         + "', Json: %s" % json_data)
        self._send_request(
            lambda: self._session.post(
                real_url, data=json_data,
                headers={"Content-Type" : "application/json"}))
        return True

    def _put_request(self, path, obj_dict, id):
        real_url = self._get_real_url(path, id=id)

        json_dict = self._get_params(obj_dict)
        json_data = json.dumps(json_dict)

        scgapi.Log.debug("Request: PUT '" + real_url
                         + "', Json: %s" % json_data)
        self._send_request(
            lambda: self._session.put(
                real_url, data=json_data,
                headers={"Content-Type" : "application/json"}))
        return True


    def _delete_request(self, path, id):
        real_url = self._get_real_url(path, id=id)

        scgapi.Log.debug("Request: DELETE '" + real_url + "'")

        self._send_request(
            lambda: self._session.delete(real_url))
        return True

    def _iterate_over(self, request_func, object_factory, offset = 0):
        self._iterations = 0
        while True:
            json_data = request_func(offset=offset)
            self._iterations += 1
            items = json_data['list']
            if not items:
                raise StopIteration()
            for item in items:
                offset += 1
                yield object_factory(item)
            if int(json_data["total"]) <= offset:
                raise StopIteration()

    def close(self):
        """Close the session and release internal resources."""

        self._session.close()
        self._session = False

