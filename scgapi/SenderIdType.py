"""
Sender Id Type

class SenderIdClass - Sender Id Type representation
class Resource - Access to list Sender Id Type

"""

import scgapi

URL_BASE = "/messaging/sender_id_types"

class SenderIdType(scgapi.ObjBase):
    """Read only object SenderIdType"""
    def __init__(self, **kwargs):
        """Constructor.

        Can be initialized empty or by specifying property
        names and values.
        """

        super(SenderIdType, self).__init__()
        self._init(**kwargs)

    def _get_member_variable_names(self):
        return ("_id", "name", "description", "capabilities",
                "allowed_mime_types", "blocked_mime_types",
                "gateway_id", "credential_parameter_list",
                "created_date", "last_update_date")

    @staticmethod
    def _create_from_json(json, resource=None):
        return scgapi.init_from_json(json, SenderIdType(), resource)

    @property
    def id(self):
        return getattr(self, "_id")

class Resource(scgapi.ResourceBase):
    """
    Access to SenderIdType.

    Methods:
        list() - List Sender Id Types
    """

    def __init__(self, session):
        super(Resource, self).__init__(
            session, URL_BASE, SenderIdType)

    def list(self, **kwargs):
        """List the SenderIdTypes"""
        return self._list(**kwargs)

