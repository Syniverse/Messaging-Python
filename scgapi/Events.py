"""
Simple events listener

The events listener require a WSGI server to handle
the actual http requests.
"""

import json
import uuid
from wsgiref import simple_server

import falcon

import scgapi

class EventsListener(object):
    def __init__(self, callback):
        self.callback = callback

    def on_get(self, req, resp):
        resp.body = '{"status": "ok - no data"}'
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        body = req.stream.read()
        if not body:
            raise falcon.HTTPBadRequest(
                'Empty request body',
                'A valid JSON document is required.')

        json_data = None
        try:
            json_data = json.loads(body.decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPError(
                falcon.HTTP_753,
                'Malformed JSON',
                'Could not decode the request body. The '
                'JSON was incorrect or not encoded as '
                'UTF-8.')

        scgapi.Log.debug("Incoming event. Json: %s" % json_data)
        if self.callback is not None:
            try:
                self.callback(json_data)
            except Exception as ex:
                scgapi.Log.error("Callback threw up: %s" % ex)

        resp.body = '{"status": "ok"}'
        resp.status = falcon.HTTP_200

