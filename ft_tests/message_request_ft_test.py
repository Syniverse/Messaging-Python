import pytest
import scgapi
import scgapi.MessageRequest
from six import string_types

class TestMessageRequests():
    @pytest.fixture(scope="class")
    def mrq(self, session, test_setup):
        message_request_id = scgapi.MessageRequest.Resource(session).create(
            from_='sender_id:'+ str(test_setup['senderIdSms']),
            to=[str(test_setup['mdnRangeStart'])],
            body='Hello World',
            test_message_flag = True)
        yield message_request_id
        try:
            scgapi.MessageRequest.Resource(session).delete(message_request_id)
        except Exception:
            pass

    def test_create(self, mrq):
        assert isinstance(mrq, string_types)
        assert mrq

    def test_list(self, session):
        num = 0
        for c in scgapi.MessageRequest.Resource(session).list():
            num += 1
            break
        assert num > 0

    def test_get(self, session, mrq, test_setup):
        message_request = scgapi.MessageRequest.Resource(session).get(mrq)
        assert message_request.id == mrq
        assert message_request.body == 'Hello World'

    def test_delete(self, session, mrq):
        scgapi.MessageRequest.Resource(session).delete(mrq)

        with pytest.raises(scgapi.HttpRequestError):
            scgapi.MessageRequest.Resource(session).get(mrq)

