
"""
Attachment

    An Attachment is a file that may be referenced my a MessageRequest
    when sending MMS or other messages that can contain file attachments,
    as well as pre-recorded audio-messages for calls.

    You will normally first create an attachment instancem, then upload a file
    (the ciontent) of the attachment, and then reference it from some other
    object (like a MessageRequest).
"""

import os.path
import mimetypes

import scgapi

URL_BASE = "/messaging/attachments"

class Attachment(scgapi.ObjBase):
    """Contact object."""

    def __init__(self, **kwargs):
        """Constructor.

        Can be initialized empty or by specifying property
        names and values.
        """

        super(Attachment, self).__init__()
        self._url_base = URL_BASE
        self._init(**kwargs)

    def _get_member_variable_names(self):
        return ("_id", "_application_id", "name", "type", "_size",
                "filename", "_state",
                "_created_date", "_last_update_date", "_version_number")

    def _get_content_path(self):
        token = self.get_session()._post_request(
            URL_BASE + "/" + self._id + "/access_tokens", {})
        return URL_BASE + "/" + token["id"] + "/content"

    @property
    def id(self):
        return getattr(self, "_id")

    @property
    def size(self):
        return getattr(self, "_size")

    @property
    def state(self):
        return getattr(self, "_state")

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
            json, Attachment(), resource)

    def change_name(self, new_name):
        args = {"name" : new_name,
                "version_number" : self._version_number}
        self.get_session()._post_request(URL_BASE, args,
                                         id=self._id,
                                         json_result=False)
        return True

    def get_download_url(self):
        """Get as (short lived) public available URL where the content can be downloaded.

        Returns:
            A string containing a URL to the attachment.
        """
        return self._get_content_path()

    def delete(self):
        """Delete the object from the database."""

        return self._delete()

    def upload(self, src_path):
        """Upload the content of the attachment from a file."""
        rval =  self.get_session()._post_file(
            self._get_content_path(), src_path, api_url="/scg-attachment/api/v1")

    def download(self, dst_path):
        """Download the content of the attachment to a file."""
        rval =  self.get_session()._get_file(
            self._get_content_path(), dst_path, api_url="/scg-attachment/api/v1")


class Resource(scgapi.ResourceImpl):
    """
    Access to Attachment.

    Methods:
        create() - Create a new Attachment
        list() - List Attachments
        get() - Get a specific Attachment
        update() - Update a contact Group
        delete() - Delete a Attachment
        create_and_upload() Creates an attachment and uploads it's content.

    """
    def __init__(self, session):
        super(Resource, self).__init__(
            session, URL_BASE, Attachment)

    def create_and_upload(self, path, **kwargs):
        """
        Create an attachment and upload a file with its content

        This is a convenience method for the most common use-case.

        Returns:
            the newly created Attachment instance (not just the id).
        """
        scgapi.Log.debug("Creating attachment. Data: '" + path + "'")

        file_len = os.path.getsize(path)

        if not "type" in kwargs:
            mime = mimetypes.guess_type(path)
            kwargs["type"] = mime[0]

        att = None
        try:
            att_id = self.create(**kwargs)
            att = self.get(att_id)
            att.upload(path)
        except Exception as ex:

            if att is not None:
               att.delete()

            raise scgapi.ApiCallFailedError()

        return self.get(att_id)
