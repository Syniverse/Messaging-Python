"""
Sender Id Class

class SenderIdClass - Sender Id Class representation
class Resource - Access to list Sender Id Classes

"""

import scgapi

URL_BASE = "/messaging/sender_id_classes"

class SenderIdClass(scgapi.ObjBase):
    """Read only object SenderIdClass."""
    def __init__(self, **kwargs):
        """Constructor.

        Can be initialized empty or by specifying property
        names and values.
        """

        super(SenderIdClass, self).__init__()
        self._init(**kwargs)

    def _get_member_variable_names(self):
        return ("_id", "name", "description", "designation",
                "applicable_countries", "country_peak_throughput",
                "country_peak_total_throughput",
                "country_daily_throughput", "delivery_window",
                "created_date", "last_update_date")

    @staticmethod
    def _create_from_json(json, resource=None):
        return scgapi.init_from_json(
            json, SenderIdClass(), resource)

    @property
    def id(self):
        return getattr(self, "_id")


class Resource(scgapi.ResourceBase):
    """
    Access to SenderIdClass.

    Methods:
        list() - List Sender Id Classes
    """

    def __init__(self, session):
        super(Resource, self).__init__(
            session, URL_BASE, SenderIdClass)

    def list(self, **kwargs):
        """List SenderIdClasses"""
        return self._list(**kwargs)
