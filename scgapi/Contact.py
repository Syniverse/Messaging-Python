"""
Contact

class Contact - Contact manipulation
class Resource - Access to Contacts

Example:
    scg = Scg()
    session = scg.connect(API_URL)
    cres = scgapi.Contact.Resource(session)
    for contact in cres.list():
        print("Name is %s" % contact.name)
"""

import scgapi


URL_BASE = "/contacts"


class ApplicationToken(scgapi.ObjBase):
    """ This resouce stores an application token
        (e.g. Push Registration ID) that is associated with the given Contact.
        It also stores information about how this token is used such as the
        associated sender Id Address and the messaging system provider."""

    def __init__(self, **kwargs):
        super(ApplicationToken, self).__init__()
        self._init(**kwargs)

    @staticmethod
    def _create_from_json(json, resource=None):
        return scgapi.init_from_json(json, ApplicationToken(), resource)

    def _get_member_variable_names(self):
        return ("_id", "sender_id_address", "message_delivery_provider",
                "token", "_application_id", "_created_date",
                "_last_update_date", "_version_number")

    @property
    def id(self):
        return getattr(self, "_id")

    @property
    def created_date(self):
        return getattr(self, "_created_date")

    @property
    def last_update_date(self):
        return getattr(self, "_last_update_date")

    @property
    def version_number(self):
        return getattr(self, "_version_number")


class AccessToken(scgapi.ObjBase):
    def __init__(self, **kwargs):
        super(AccessToken, self).__init__()
        self._init(**kwargs)

    @staticmethod
    def _create_from_json(json, resource=None):
        return scgapi.init_from_json(json, AccessToken(), resource)

    def _get_member_variable_names(self):
        return ("_id", "duration", "_expiry_time", "_application_id", "_created_date",
                "_last_update_date", "_version_number")

    @property
    def id(self):
        return getattr(self, "_id")

    @property
    def expiry_time(self):
        return getattr(self, "_expiry_time")

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


class Address(scgapi.ObjBase):
    """An extra, optional address for a Contact."""

    def __init__(self, **kwargs):
        super(Address, self).__init__()
        self._init(**kwargs)


    @staticmethod
    def _create_from_json(json):
        return scgapi.init_from_json(json, Address())

    def _get_member_variable_names(self):
        return ("priority", "designation", "use", "source", "status",
                "line1", "line2", "city", "state", "province", "zip",
                "country")


class Account(scgapi.ObjBase):
    """An extra, optional account."""

    def __init__(self, **kwargs):
        super(Account, self).__init__()
        self._init(**kwargs)

    def _get_member_variable_names(self):
        return ("priority", "designation", "source", "state",
                "username", "domain", "access_token")


    @staticmethod
    def _create_from_json(json):
        return scgapi.init_from_json(json, Account())


class Device(scgapi.ObjBase):
    """A device used by a Contact."""

    def __init__(self, **kwargs):
        super(Device, self).__init__()
        self._init(**kwargs)

    def _get_member_variable_names(self):
        return ("priority", "designation", "source", "state",
                "msisdn", "carrier", "mac_address", "uuid",
                "manufacturer", "model", "os")

    @staticmethod
    def _create_from_json(json):
        return scgapi.init_from_json(json, Device())


class Demographic(scgapi.ObjBase):
    """Demographic data."""

    def __init__(self, **kwargs):
        super(Demographic, self).__init__()
        self._init(**kwargs)

    def _get_member_variable_names(self):
        return ("name", "source", "score")

    @staticmethod
    def _create_from_json(json):
        return scgapi.init_from_json(json, Demographic())


class Interest(scgapi.ObjBase):
    """An interest by a Contact."""

    def __init__(self, **kwargs):
        super(Interest, self).__init__()
        self._init(**kwargs)

    def _get_member_variable_names(self):
        return ("code", "name", "source", "score")

    @staticmethod
    def _create_from_json(json):
        return scgapi.init_from_json(json, Interest())


class Contact(scgapi.ObjBase):
    """Contact object."""

    def __init__(self, **kwargs):
        """Constructor.

        Can be initialized empty or by specifying property names
        and values.
        """

        super(Contact, self).__init__()
        self._init(**kwargs)

    def _get_member_variable_names(self):
        return ("_id", "external_id", "first_name", "last_name",
                "birth_date", "first_acquisition_date",
                "last_acquisition_date", "primary_mdn",
                "primary_addr_line1", "primary_addr_line2",
                "primary_addr_city", "primary_addr_zip",
                "primary_addr_state", "primary_email_addr",
                "primary_social_handle", "address_list",
                "account_list", "device_list", "interest_list",
                "demographic_list", "extended_attributes",
                "social_handles", "preferred_language", "voice_preference",
                "fast_access", "_application_id", "_created_date",
                "_last_update_date", "_version_number", "fast_access_1",
                "fast_access_2", "fast_access_3", "fast_access_4",
                "fast_access_5", "fast_access_6", "fast_access_7",
                "fast_access_8", "fast_access_9", "fast_access_10",
                "fast_access_11", "fast_access_12", "fast_access_13",
                "fast_access_14", "fast_access_15", "fast_access_16",
                "fast_access_17", "fast_access_18", "fast_access_19",
                "fast_access_20")

    def _get_lists(self):
        return {"address_list" : Address._create_from_json,
                "account_list" : Account._create_from_json,
                "device_list" : Device._create_from_json,
                "interest_list" : Interest._create_from_json,
                "demographic_list" : Demographic._create_from_json}

    @property
    def id(self):
        return getattr(self, "_id")

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
        contact = Contact()

        if resource is not None:
            contact.set_resource(resource)

        lists = contact._get_lists()

        for key in contact._get_member_variable_names():
            if key.startswith("_"):
                setattr(contact, key, json.get(key[1:], None))
            elif key in lists:
                setattr(contact, key, scgapi.add_list_from_json(
                    json, key, lists[key]))
            else:
                setattr(contact, key, json.get(key, None))
        return contact


    def update(self):
        """Update the object in the database."""

        return self._update()

    def delete(self):
        """Delete the object from the database."""

        return self._delete()

    def _get_application_tokens_path(self):
        return URL_BASE + "/" + self._id + "/application_tokens"

    def get_application_token_resource(self):
        """Resource to ApplicationToken objects that provides:

            create() - Create a new ApplicationToken
            list() - List ApplicationTokens
            get() - Get a specific ApplicationToken
            update() - Update an ApplicationToken
            delete() - Delete an ApplicationToken

        """
        return _ApplicationTokenResource(self.get_session(), self._get_application_tokens_path())

    def _get_access_tokens_path(self):
        return URL_BASE + "/" + self._id + "/access_tokens"

    def get_access_token_resource(self):
        """Resource to AccessToken objects that provides:

            create() - Create a new AccessToken
            list() - List AccessTokens
            get() - Get a specific AccessToken
            delete() - Delete an AccessToken

        """
        return _AccessTokenResource(self.get_session(), self._get_access_tokens_path())


class Resource(scgapi.ResourceImpl):
    """
    Access to Contact.

    Methods:
        create() - Create a new Contact
        list() - List Contacts
        get() - Get a specific Contact
        update() - Update a Sontact
        delete() - Delete a Contact

    """

    def __init__(self, session):
        super(Resource, self).__init__(session, URL_BASE, Contact)

class _ApplicationTokenResource(scgapi.ResourceImpl):
    """
    Access to ApplicationToken.

    Methods:
        create() - Create a new ApplicationToken
        list() - List ApplicationTokens
        get() - Get a specific Contact
        update() - Update a ApplicationToken
        delete() - Delete a ApplicationToken

    """

    def __init__(self, session, url):
        super(_ApplicationTokenResource, self).__init__(session, url, ApplicationToken)

class _AccessTokenResource(scgapi.ResourceBase):
    """
    Access to AccessToken.

    Methods:
        create() - Create a new AccessToken
        list() - List AccessTokens
        get() - Get a specific AccessToken
        delete() - Delete a AccessToken
    """

    def list(self, **kwargs):
        return self._list(**kwargs)

    def get(self, id):
        return self._get(id)

    def create(self, **kwargs):
        return self._create(**kwargs)

    def delete(self, obj):
        return self._delete(obj)

    def __init__(self, session, url):
        super(_AccessTokenResource, self).__init__(session, url, AccessToken)