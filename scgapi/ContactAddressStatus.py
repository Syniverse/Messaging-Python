"""
ContactAddressStatus

class ContactAddressStatus - ContactAddressStatus manipulation
class Resource - Access to ContactAddressStatuss

Example:
    scg = Scg()
    session = scg.connect(API_URL)
    cres = scgapi.ContactAddressStatus.Resource(session)
    for cas in cres.list():
        print("CAS is %s" % cas.address)
"""

import scgapi


URL_BASE = "/consent/contact_address_statuses"


class ContactAddressStatus(scgapi.ObjBase):
    """ContactAddressStatus object."""

    def __init__(self, **kwargs):
        """Constructor.

        Can be initialized empty or by specifying property names
        and values.
        """

        super(ContactAddressStatus, self).__init__()
        self._init(**kwargs)

    def _get_member_variable_names(self):
        return ("_id", "address_type", "address", "sender_id",
                "_consent_status", "_application_id", "_created_date",
                "_last_update_date", "_version_number")
    @property
    def id(self):
        return getattr(self, "_id")

    @property
    def consent_status(self):
        return getattr(self, "_consent_status")

    @property
    def application_id(self):
        return getattr(self, "_application_id")

    @property
    def created_date(self):
        return getattr(self, "_created_date")

    @property
    def last_update_date(self):
        return getattr(self, "_last_update_date")

    @property
    def version_number(self):
        return getattr(self, "version_number")

    @staticmethod
    def _create_from_json(json, resource=None):
         return scgapi.init_from_json(
            json, ContactAddressStatus(), resource)

    def delete(self):
        """Delete the object from the database."""

        return self._delete()

    def set_consent(self, consent_status):
        """Set the consent status

        Args:
            consent_status: (str) One of  'NONE', 'OPTIN', 'OPTOUT', 'BLACKLIST' or 'WHITELIST'
        """
        args = {"consent_status" : consent_status,
                "version_number" : self._version_number}
        result = self.get_session()._post_request(
            URL_BASE, args, id=self._id, json_result=False)
        return True


class Resource(scgapi.ResourceBase):
    """
    Access to ContactAddressStatus.

    Methods:
        create() - Create a new ContactAddressStatus
        list() - List ContactAddressStatus
        get() - Get a specific ContactAddressStatus
        delete() - Delete the ContactAddressStatus
    """

    def __init__(self, session):
        super(Resource, self).__init__(session, URL_BASE, ContactAddressStatus)

    def list(self, **kwargs):
        return self._list(**kwargs)

    def get(self, id):
        return self._get(id)

    def create(self, **kwargs):
        return self._create(**kwargs)

    def delete(self, id):
        return self._delete(id)
