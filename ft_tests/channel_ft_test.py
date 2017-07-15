
import pytest
import scgapi
import scgapi.Channel
from six import string_types

class TestChannels():
    @pytest.fixture(scope="class")
    def cid(self, session):
        channel_id = scgapi.Channel.Resource(session).create(name='CRUD channel',
                                                       description='Test')
        yield channel_id
        try:
            scgapi.Channel.Resource(session).delete(channel_id)
        except Exception:
            pass

    def test_create(self, cid):
        assert isinstance(cid, string_types)
        assert cid

    def test_list(self, session):
        num = 0
        for c in scgapi.Channel.Resource(session).list():
            num += 1
            break
        assert num > 0

    def test_get(self, session, cid):
        channel = scgapi.Channel.Resource(session).get(cid)
        assert channel.id == cid
        assert channel.description == 'Test'

    def test_update(self, session, cid):
        channel = scgapi.Channel.Resource(session).get(cid)
        channel.name = 'Testing'
        channel.update()
        updated = scgapi.Channel.Resource(session).get(cid)
        assert updated.id == cid
        assert updated.name == 'Testing'

    def test_delete(self, session, cid):
        scgapi.Channel.Resource(session).delete(cid)

        with pytest.raises(scgapi.HttpRequestError):
            scgapi.Channel.Resource(session).get(cid)

