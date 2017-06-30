"""
Bridge

class Bridge - Bridge manipulation
class Resource - Access to Bridges
"""

import scgapi
import scgapi.SenderId

URL_BASE = "/calling/bridges"

class Bridge(scgapi.ObjBase):

    def __init__(self, **kwargs):
        """Constructor.

        Can be initialized empty or by specifying property
        names and values.
        """

        super(Bridge, self).__init__()
        self._url_base = URL_BASE
        self._init(**kwargs)

    def _get_member_variable_names(self):
        return ("_id", "_external_id", "call_ids", "state",
            "bridge_audio", "_completed_time", "_activated_time",
            "_created_date",
            "_last_updated_date", "_version_number")

    @property
    def id(self):
        return getattr(self, "_id")

    @property
    def external_id(self):
        return getattr(self, "_external_id")

    @property
    def completed_time(self):
        return getattr(self, "_completed_time")

    @property
    def activated_time(self):
        return getattr(self, "_activated_time")

    @property
    def created_date(self):
        return getattr(self, "_created_date")

    @property
    def last_update_date(self):
        return getattr(self, "_last_update_date")

    @property
    def version_number(self):
        return getattr(self, "_version_number")

    @staticmethod
    def _create_from_json(json, resource=None):
        return scgapi.init_from_json(
            json, Bridge(), resource)


class Resource(scgapi.ResourceBase):
    """
    Access to Bridge.

    Methods:
        create() - Create a new Bridge
        list() - List Bridges
        get() - Get a specific Bridge
    """
    def __init__(self, session):
        super(Resource, self).__init__(
            session, URL_BASE, scgapi.Bridge.Bridge)

    def create(self, **kwargs):
        """Create a bridge."""
        return self._create(**kwargs)

    def list(self, **kwargs):
        """List bridges."""
        return self._list(**kwargs)

    def get(self, id):
        """Get the instance for a specific bridge.

        Args:
            id (str): The id for an existing bridge.
        """
        return self._get(id)