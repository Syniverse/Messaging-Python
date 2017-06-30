"""
Message object

The messages are generated on the server side after creating a MessageRequest,
and are read-only objects. The only valid operations are some state changes
and delete().

class Message - Message manipulation
class Resource - Access to Messages

Example:
    scg = Scg()
    session = scg.connect(API_URL)
    msg_res = scgapi.Message.Resource(session)
    for msg in smg_res.list():
        print("Subject is %s" % msg.subject)
"""

import scgapi
import scgapi.Attachment

URL_BASE = "/messaging/messages"

class MessageFragmentInfo(scgapi.ObjBase):
    def __init__(self, **kwargs):
        super(MessageFragmentInfo, self).__init__()
        self._init(**kwargs)

    @staticmethod
    def _create_from_json(json):
        return scgapi.init_from_json(json, MessageFragmentInfo())

    def _get_member_variable_names(self):
        return ("fragment_id", "fragment_state", "charge", "failure_code",
                "failure_details", "protocol_error", "external_id",
                "delivery_report_reference")

class Message(scgapi.ObjBase):
    """Contact object."""

    def __init__(self, **kwargs):
        """Constructor.

        Can be initialized empty or by specifying property
        names and values.
        """

        super(Message, self).__init__()
        self._url_base = URL_BASE
        self._init(**kwargs)

    def _get_member_variable_names(self):
        return (
            "_id", "message_request_id", "external_transaction_ids",
            "external_message_request_id",
            "application_id", "application_tracking_id",
            "conversation_id", "campaign_id", "direction",
            "customer_sender_id ", "from_address", "to_address",
            "state", "failure_code", "failure_details", "subject",
            "body", "sent_date", "delivered_date", "converted_date",
            "conversion_info_source", "reply_to", "attachments",
            "type", "message_delivery_provider", "contact_id", "price",
            "language", "failed_translation", "protocol_error",
            "scheduled_delivery_time", "expiry_time", "failed_origin_id",
            "failover", "created_date", "last_update_date", "_fragments_info",
            "consent_requirement")

    def _get_lists(self):
        return {"_fragments_info" : MessageFragmentInfo._create_from_json}

    def _get_attachments_path(self):
        return URL_BASE + "/" + self._id + "/attachments"

    @property
    def id(self):
        return getattr(self, "_id")

    @property
    def fragments_info(self):
        return getattr(self, "_fragments_info")

    @staticmethod
    def _create_from_json(json, resource=None):
        message = Message()

        if resource is not None:
            message.set_resource(resource)

        lists = message._get_lists()

        for key in message._get_member_variable_names():
            if key in lists:
                # NB: Assumes the list starts with _ (read only)
                setattr(message, key, scgapi.add_list_from_json(
                    json, key[1:], lists[key]))
            elif key.startswith("_"):
                setattr(message, key, json.get(key[1:], None))
            else:
                setattr(message, key, json.get(key, None))
        return message

    def _set_state(self, state):
        self.get_session()._post_request(
            URL_BASE + "/" + self._id,
            {"state":state})
        self._state = state

    def set_state_processed(self):
        self.set_state("PROCESSED")

    def set_state_converted(self):
        self.set_state("CONVERTED")

    def delete(self):
        """Delete the object from the database."""

        return self._delete()

    def list_attachments(self, **kwargs):
        """List the attachments for this Message"""
        att = scgapi.Attachment.Attachment()
        return self.get_session()._iterate_over(
            lambda offset: self.get_session()._get_request(
                self._get_attachments_path(),
                att.wash_args(**kwargs),
                offset=offset),
            lambda json: att._create_from_json(json, self))



class Resource(scgapi.ResourceBase):
    """
    Access to Message.

    Methods:
        list() - List Messages
        get() - Get a specific Message
        delete() - Delete a Message

    """
    def __init__(self, session):
        super(Resource, self).__init__(
            session, URL_BASE, Message)

    def list(self, **kwargs):
        return self._list(**kwargs)

    def get(self, id):
        return self._get(id)

    def delete(self, obj):
        return self._delete(obj)
