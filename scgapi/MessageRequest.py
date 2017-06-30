"""
MessageRequest

class MessageRequest - Sending mesages using the API
class Resource - Access to MessageRequests

"""

import scgapi
import scgapi.Message

URL_BASE = "/messaging/message_requests"



class MessageRequest(scgapi.ObjBase):
    """MessageRequest object."""

    def __init__(self, **kwargs):
        """Constructor.

        Can be initialized empty or by specifying property names
        and values.
        """

        super(MessageRequest, self).__init__()
        self._init(**kwargs)

    def _get_member_variable_names(self):
        return ("_id",
                "from", "conversation_id", "to", "campaign_id",
                "program_id", "subject", "application_id",
                "external_id", "_state", "attachments", "body",
                "consent_requirement", "criteria",
                "_recipient_count", "_sent_count",
                "_delivered_count", "_read_count",
                "_converted_count", "_canceled_count",
                "_failed_count", "scheduled_delivery_time",
                "scheduled_delivery_time_zone", "expiry_time",
                "test_message_flag", "pause_before_transmit",
                "contact_delivery_address_priority", "failover",
                "price_threshold", "sender_id_sort_criteria",
                "src_language", "dst_language", "translate",
                "_translations_count", "_translations_failed_count",
                "_translations_performed_count",
                "pause_expiry_time", "_created_date",
                "_last_update_date")

    def _get_messages_path(self):
        return URL_BASE + "/" + self._id + "/messages"

    @property
    def id(self):
        return getattr(self, "_id")

    @property
    def state(self):
        return getattr(self, "_state")

    @property
    def recipient_count(self):
        return getattr(self, "_recipient_count")

    @property
    def sent_count(self):
        return getattr(self, "_sent_count")

    @property
    def delivered_count(self):
        return getattr(self, "_delivered_count")

    @property
    def read_count(self):
        return getattr(self, "_read_count")

    @property
    def converted_count(self):
        return getattr(self, "_converted_count")

    @property
    def canceled_count(self):
        return getattr(self, "_canceled_count")

    @property
    def failed_count(self):
        return getattr(self, "_failed_count")

    @property
    def translations_count(self):
        return getattr(self, "_translations_count")

    @property
    def translations_failed_count(self):
        return getattr(self, "_translations_failed_count")

    @property
    def translations_performed_count(self):
        return getattr(self, "_translations_performed_count")

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
            json, MessageRequest(), resource)

    def delete(self):
        """Delete the object from the database."""

        return self._delete()

    def _set_state(self, state):
        self.get_session()._post_request(
            URL_BASE + "/" + self._id,
            {"state":state})
        self._state = state

    def resume(self):
        """Resume the generation of messages"""
        return self._set_state("TRANSMITTING")

    def cancel(self):
        """Cancel the generation of messages"""
        return self._set_state("CANCELED")

    def list_messages(self, **kwargs):
        msg = scgapi.Message.Message()
        return self.get_session()._iterate_over(
            lambda offset: self.get_session()._get_request(
                self._get_messages_path(),
                msg.wash_args(**kwargs),
                offset=offset),
            lambda json: msg._create_from_json(json, self))



class Resource(scgapi.ResourceBase):
    """
    Access to MessageRequest.

    Methods:
        create() - Create a new MessageRequest
        list() - List MessageRequest
        get() - Get a specific MessageRequest
        delete() - Delete a MessageRequest

    """

    def __init__(self, session):
        super(Resource, self).__init__(
            session, URL_BASE, MessageRequest)

    def list(self, **kwargs):
        """List MessageRequests"""
        return self._list(**kwargs)

    def get(self, id):
        """Get a specific MessageRequest"""
        return self._get(id)

    def create(self, **kwargs):
        """Create a MessageRequest

        This will instruct the server to generate and send or queue Message(s).

        """
        return self._create(**kwargs)

    def delete(self, obj):
        """Delete a MessageRequest"""
        return self._delete(obj)
