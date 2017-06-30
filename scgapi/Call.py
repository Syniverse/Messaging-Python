"""
Call

class Call - Call manipulation
class Resource - Access to Calls

"""

import scgapi
import scgapi.SenderId

URL_BASE = "/calling/calls"

class Call(scgapi.ObjBase):

    def __init__(self, **kwargs):
        """Constructor.

        Can be initialized empty or by specifying property
        names and values.
        """

        super(Call, self).__init__()
        self._url_base = URL_BASE
        self._init(**kwargs)

    def _get_member_variable_names(self):
        return ("_id", "external_id", "from", "from_address", "recording_enabled",
            "to", "answer_timeout", "state","direction", "_start_time",
            "_answer_time", "_end_time", "_chargeable_duration", "bridge_id",
            "_failure_code", "_failure_details", "_created_date",
            "_last_updated_date", "_version_number")

    @property
    def id(self):
        return getattr(self, "_id")

    @property
    def start_time(self):
        return getattr(self, "_start_time")

    @property
    def answer_time(self):
        return getattr(self, "_answer_time")

    @property
    def end_time(self):
        return getattr(self, "_end_time")

    @property
    def chargeable_duration(self):
        return getattr(self, "_chargeable_duration")

    @property
    def failure_code(self):
        return getattr(self, "_failure_code")

    @property
    def failure_details(self):
        return getattr(self, "_failure_details")

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
            json, Call(), resource)

    def _get_play_path(self):
        return self._url_base + "/" + self._id + "/play_audio"

    def play(self, path):
        """Play a pre-defined audio file to the call.

        The recording will be played almost immediately.

        Args:
            path (str): Attachment id or the URL where the recording can be  streamed (downloaded) from.
        """
        url_type = "ATTACHMENT"
        if path.startswith("http://") or path.startswith("https://"):
            url_type = "URL"
        session = self.get_session()
        session._post_request(
            self._get_play_path(),
            {"source_type":url_type,
             "source":path})


class Resource(scgapi.ResourceBase):
    """
    Access to Call.

    Methods:
        create() - Create a new Call
        list() - List Calls
        get() - Get a specific Call
    """
    def __init__(self, session):
        super(Resource, self).__init__(
            session, URL_BASE, scgapi.Call.Call)

    def create(self, **kwargs):
        """Create a Call."""
        return self._create(**kwargs)

    def list(self, **kwargs):
        """List calls."""
        return self._list(**kwargs)

    def get(self, id):
        """Get the instance of an existing call.

        Args:
            id (str): Id of an existing Call.
        """
        return self._get(id)
