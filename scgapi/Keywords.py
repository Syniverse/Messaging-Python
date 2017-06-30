"""
Keywords

class Keywords - Keywords manipulation
class Resource - Access to Keywordss

Example:
    scg = Scg()
    session = scg.connect(API_URL)
    res = scgapi.Keywords.Resource(session)
    for kw in res.list():
        print("Name is %s" % kw.name)
"""

import scgapi
from scgapi.Contact import Contact

URL_BASE = "/messaging/keywords"

class Keywords(scgapi.ObjBase):
    """Keywords object."""

    def __init__(self, **kwargs):
        """Constructor.

        Can be initialized empty or by specifying property
        names and values.
        """

        super(Keywords, self).__init__()
        self._url_base = URL_BASE
        self._init(**kwargs)

    def _get_member_variable_names(self):
        return ("_id", "name", "description", "value", "case",
                "sender_id", "valid_from", "valid_to",
                "associated_info", "campaign_id", "type",
                "actions", "reply_template", "_application_id",
                "_created_date", "_last_update_date", "_version_number")

    def _get_contacts_path(self):
        return self._url_base + "/" + self._id + "/contacts"

    @property
    def id(self):
        return getattr(self, "_id")

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

    @staticmethod
    def _create_from_json(json, resource=None):
        return scgapi.init_from_json(json, Keywords(), resource)

    def update(self):
        """Update the object in the database."""

        return self._update()

    def delete(self):
        """Delete the object from the database."""

        return self._delete()


class Resource(scgapi.ResourceImpl):
    """
    Access to Keywords.

    Methods:
        create() - Create a new Keywords
        list() - List Keywordss
        get() - Get a specific Keywords
        update() - Update a contact Group
        delete() - Delete a Keywords

    """

    def __init__(self, session):
        super(Resource, self).__init__(
            session, URL_BASE, Keywords)
