"""
Contact Group

class ContactGroup - Contact Group manipulation
class Resource - Access to Contact Groups

Example:
    scg = Scg()
    session = scg.connect(API_URL)
    cg_res = scgapi.ContactGroup.Resource(session)
    for contact_group in cg_res.list():
        print("Name is %s" % contact_group.name)
"""

import scgapi
from scgapi.Contact import Contact

URL_BASE = "/contact_groups"

class ContactGroup(scgapi.ObjBase):
    """Contact Group object."""

    def __init__(self, **kwargs):
        """Constructor.

        Can be initialized empty or by specifying property
        names and values.
        """

        super(ContactGroup, self).__init__()
        self._url_base = URL_BASE
        self._init(**kwargs)

    def _get_member_variable_names(self):
        return ("_id", "external_id", "name", "description",
                "_status", "_member_count", "_created_date",
                "criteria", "_application_id",
                "_last_update_date", "_version_number", "_type")

    def _get_contacts_path(self):
        return self._url_base + "/" + self._id + "/contacts"

    @property
    def id(self):
        return getattr(self, "_id")

    @property
    def status(self):
        return getattr(self, "_status")

    @property
    def type(self):
        return getattr(self, "_type")

    @property
    def application_id(self):
        return getattr(self, "_application_id")

    @property
    def member_count(self):
        return getattr(self, "_member_count")

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
        return scgapi.init_from_json(json, ContactGroup(), resource)

    def list_contacts(self, **kwargs):
        """
        List contacts in the Contact Group.

        Filters may be applied.

        Returns a generator that provides contact instances for
        all the contacts in the Contact Group (that matches the
        filter if are applied).
        """

        session = self.get_session()
        return session._iterate_over(
            lambda offset: session._get_request(
                self._get_contacts_path(),
                Contact().wash_args(**kwargs),
                offset=offset),
            lambda json: Contact._create_from_json(
                json, self.get_resource()))

    def add_contact(self, contact_id):
        """
        Add a contact to a Contact Group

        Note that if a list of contacts are added, some contacts
        may be added while others fail. In that case, a
        scgapi.ApiCallFailedError will be raised, and a json list
        of failed contact id's will be returned in the
        exceptions text message. Example of error when trying to
        add non-existing contacts:

            {'errors': {'some_id1': 'Unknown document: some_id1',
            'some_id2': 'Unknown document: some_id2'}}

        :param contact_id: A string with a contact id, or a
            list of strings with contact id's to add.
        :returns: True if the operation went well.
        """

        session = self.get_session()
        if isinstance(contact_id, list):
            args = {"contacts": contact_id}
            rval = session._post_request(
                self._get_contacts_path(), args)
            if "errors" in rval and any(rval["errors"]):
                raise scgapi.ApiCallFailedError(rval)
        else:
            one_id = [contact_id]
            return self.add_contact(one_id)

        return True

    def delete_contact(self, contact_id):
        """

        Delete a reference to a Contact for this group.

        The Contact object itself remains unharmed.

        :param contact_id: An id (str) for a Contact, or
            a Contact instance.
        """

        if isinstance(contact_id, Contact):
            id = contact_id._id
        else:
            id = contact_id # assume string
        return self.get_session()._delete_request(
            self._get_contacts_path(), id)

    def update(self):
        """Update the object in the database."""

        return self._update()

    def delete(self):
        """Delete the object from the database."""

        return self._delete()


class Resource(scgapi.ResourceImpl):
    """
    Access to ContactGroup.

    Methods:
        create() - Create a new Contact Group
        list() - List Contact Groups
        get() - Get a specific Contact Group
        update() - Update a contact Group
        delete() - Delete a Contact Group

    """

    def __init__(self, session):
        super(Resource, self).__init__(
            session, URL_BASE, ContactGroup)
