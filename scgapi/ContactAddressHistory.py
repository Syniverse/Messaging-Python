"""
ContactAddressHistory

class ContactAddressHistory - ContactAddressHistory manipulation
class Resource - Access to ContactAddressHistorys
"""

import scgapi

URL_BASE = "/consent/contact_address_history"

class ContactAddressHistory(scgapi.ObjBase):
    """ContactAddressHistory object."""

    def __init__(self, **kwargs):
        """Constructor.

        Can be initialized empty or by specifying property names
        and values.
        """

        super(ContactAddressHistory, self).__init__()
        self._init(**kwargs)

    def _get_member_variable_names(self):
        return ("_id", "msisdn", "sender_id", "source", "status",
                "timestamp", "message", "keyword", "application_id"
                "created_date", "last_update_date", "version_number")

    @property
    def id(self):
        return getattr(self, "_id")

    @staticmethod
    def _create_from_json(json, resource=None):
         return scgapi.init_from_json(
            json, ContactAddressHistory(), resource)


class Resource(scgapi.ResourceBase):
    """
    Access to ContactAddressHistory.

    Methods:
        create() - Create a new ContactAddressHistory
        list() - List ContactAddressHistory
        get() - Get a specific ContactAddressHistory

    """

    def __init__(self, session):
        super(Resource, self).__init__(session, URL_BASE, ContactAddressHistory)

    def list(self, **kwargs):
        return self._list(**kwargs)
