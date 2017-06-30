"""
Sender Id

class SenderId - Sender Id manipulation
class Resource - Access to list Sender Ids

"""

import scgapi
from scgapi.Contact import Contact

URL_BASE = "/messaging/sender_ids"

class ProvisionSenderId(scgapi.ObjBase):
    """Implementation detail"""
    def __init__(self, **kwargs):
        """Constructor.

        Can be initialized empty or by specifying property
        names and values.
        """

        super(ProvisionSenderId, self).__init__()
        self._init(**kwargs)

    def _get_member_variable_names(self): \
            return ("state", "version_number")

    @staticmethod
    def _create_from_json(json, resource=None):
        return scgapi.init_from_json(
            json, ProvisionSenderId(), resource)


class SenderId(scgapi.ObjBase):
    """SenderId"""

    def __init__(self, **kwargs):
        """Constructor.

        Can be initialized empty or by specifying property
        names and values.
        """

        super(SenderId, self).__init__()
        self._init(**kwargs)

    def _get_member_variable_names(self):
        return ("_id", "parent_id", "name", "ownership", "class_id",
                "type_id", "state", "address", "content_type",
                "message_templates", "country", "operators",
                "credentials", "two_way_required",
                "keep_sender_address", "dr_required",
                "consent_managed_by", "capabilities",
                "check_whitelist", "billing", "_application_id",
                "_created_date", "_last_update_date", "_version_number")

    @staticmethod
    def _create_from_json(json, resource=None):
        return scgapi.init_from_json(
            json, SenderId(), resource)

    @property
    def id(self):
        return getattr(self, "_id")

    @property
    def type(self):
        return getattr(self, "_type")

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
        return getattr(self, "_version_number")

    def activate(self):
        """Activate the SenderId"""
        self.get_resource().set_state(self.id, self.version_number, "ACTIVE")

    def deactivate(self):
        """Deactivete the SenderId"""
        self.get_resource().set_state(self.id, self.version_number, "INACTIVE")


class Resource(scgapi.ResourceImpl):
    """
    Access to SenderId

    Methods:
        create() - Create a new Sender Id
        list() - List Sender Ids
        get() - Get a specific Sender Id
        update() - Update a contact Group
        delete() - Delete a Sender Id
        purchase() - Creates a new Sender ID Resource

    """

    def __init__(self, session):
        super(Resource, self).__init__(session, URL_BASE, SenderId)

    def purchase(self, parent_id):
        """
        Creates a new Sender ID Resource, copy of specified
        PREPROVISIONED Sender ID, which becomes PURCHASED
        until the private copy is deleted.
        """

        url = URL_BASE + "/purchase"
        rval = self._session._post_request(
            url,
            self._cls().wash_args(**kwargs))
        return rval["id"]

    def set_state(self, id, version, activate):
        state = ProvisionSenderId()
        kwargs = {"state":activate, "version_number":version}

        url = URL_BASE + "/" + id
        self._session._post_request(
            url,
            state.wash_args(**kwargs))

