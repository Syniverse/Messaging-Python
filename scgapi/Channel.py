"""
Channel

class Channel - Channel manipulation
class Resource - Access to Channels

Example:
    scg = Scg()
    session = scg.connect(API_URL)
    mt_res = scgapi.Channel.Resource(session)
    for mt in mt_res.list():
        print("Name is %s" % mt.name)
"""

import scgapi
import scgapi.SenderId

URL_BASE = "/messaging/channels"

class Channel(scgapi.ObjBase):

    def __init__(self, **kwargs):
        """Constructor.

        Can be initialized empty or by specifying property
        names and values.
        """

        super(Channel, self).__init__()
        self._url_base = URL_BASE
        self._init(**kwargs)

    def _get_member_variable_names(self):
        return ("_id", "name", "priority", "role",
                "description", "_ownership", "_application_id",
                "_created_date", "_last_update_date",
                "_version_number", "message_templates")

    @property
    def id(self):
        return getattr(self, "_id")

    @property
    def ownership(self):
        return getattr(self, "_ownership")

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
        return scgapi.init_from_json(
            json, Channel(), resource)

    def _get_senderids_path(self):
        return self._url_base + "/" + self._id + "/sender_ids"

    def list_sender_ids(self, **kwargs):
        """
        List Sender ID's in the Channel

        Filters may be applied.

        Returns a generator that provides SenderID instances for
        all the Sender Id's in the XChannel (that matches the
        filter if filers are applied).
        """

        session = self.get_session()
        return session._iterate_over(
            lambda offset: session._get_request(
                self._get_senderids_path(),
                scgapi.SenderId.SenderId().wash_args(**kwargs),
                offset=offset),
            lambda json: Contact._create_from_json(
                json, self.get_resource()))

    def add_sender_id(self, sender_id):
        """
        Add one or more Sender Id's to a Channel

        Note that if a list of senedr id's are added, some
        may be added while others fail. In that case, a
        scgapi.ApiCallFailedError will be raised, and a json list
        of failed contact id's will be returned in the
        exceptions text message.

        :param sender_id: A string with a sender id, or a
            list with sender-id's.
        :returns: True if the operation went well.
        """

        session = self.get_session()
        if isinstance(sender_id, list):
            args = {"sender_ids": sender_id}
            rval = session._post_request(
                self._get_senderids_path(), args)
            if rval and "errors" in rval and any(rval["errors"]):
                raise scgapi.ApiCallFailedError(rval)
        else:
            one_id = [sender_id]
            return self.add_sender_id(one_id)

        return True

    def delete_sender_id(self, sender_id):
        """

        Delete a reference to a Contact for this group.

        The Contact object itself remains unharmed.

        :param sender_id: An id (str) for a Contact, or
            a Contact instance.
        """

        if isinstance(sender_id, scgapi.SenderId.SenderId):
            id = sender_id._id
        else:
            id = sender_id # assume string
        return self.get_session()._delete_request(
            self._get_senderids_path(), id)

    def update(self):
        """Update the object in the database."""

        return self._update()

    def delete(self):
        """Delete the object from the database."""

        return self._delete()


class Resource(scgapi.ResourceImpl):
    """
    Access to Channel.

    Methods:
        create() - Create a new Channel
        list() - List Channels
        get() - Get a specific Channel
        update() - Update a contact Group
        delete() - Delete a Channel

    """
    def __init__(self, session):
        super(Resource, self).__init__(
            session, URL_BASE, scgapi.Channel.Channel)
