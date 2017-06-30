"""
Message Template

class MessageTemplate - Message Template manipulation
class Resource - Access to Message Templates

"""

import scgapi

URL_BASE = "/messaging/message_templates"

class MessageTemplate(scgapi.ObjBase):
    """MessageTemplate object"""

    def __init__(self, **kwargs):
        """Constructor.

        Can be initialized empty or by specifying property
        names and values.
        """

        super(MessageTemplate, self).__init__()
        self._url_base = URL_BASE
        self._init(**kwargs)

    def _get_member_variable_names(self):
        return ("_id", "designation", "name", "pattern", "_application_id",
                "_created_date", "_last_update_date")

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

    @staticmethod
    def _create_from_json(json, resource=None):
        return scgapi.init_from_json(
            json, MessageTemplate(), resource)

    def update(self):
        """Update the object in the database."""

        return self._update()

    def delete(self):
        """Delete the object from the database."""

        return self._delete()


class Resource(scgapi.ResourceImpl):
    """
    Access to MessageTemplate.

    Methods:
        create() - Create a new Message Template
        list() - List Message Templates
        get() - Get a specific Message Template
        update() - Update a Message Template
        delete() - Delete a Message Template

    """
    def __init__(self, session):
        super(Resource, self).__init__(
            session, URL_BASE, MessageTemplate)
