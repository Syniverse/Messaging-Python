"""
Event listener example.

The (very simple) scgapi.Events module is implemented
using the minimalistic, but fast, Falcon library
[http://falconframework.org/]. This uses WSGI, which gives us a great
flexibility in regard of what http server we want to use. For
production, you can use Apache, Nginx or a number of other robust
http servers. For testing, we have used gunicorn for this project.

Example:
    $ gunicorn -b 10.0.1.100:8000 events_listener

The example above starts a http service on port 8000 on 10.0.1.100.
You can the acces the api at URL: "http://10.0.1.100/events".
"""

import logging

import falcon
import scgapi.Events

from scgapi.Scg import Scg

def callback(data):
    print("Incoming data: %s" % data)

# Set log options
scg = Scg(log=True, log_level=logging.DEBUG)

# Falcon setup.
handler = scgapi.Events.EventsListener(callback)
application = falcon.API()
application.add_route('/events', handler)

