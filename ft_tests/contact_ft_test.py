import pytest
import scgapi
import scgapi.Contact
from six import string_types

class TestContacts():
    @pytest.fixture(scope="class")
    def uid(self, session, test_setup):
        contact_id = scgapi.Contact.Resource(session).create(
            first_name='test', last_name='User',
            primary_mdn=str(test_setup['mdnRangeStart']))
        yield contact_id
        try:
            scgapi.Contact.Resource(session).delete(contact_id)
        except Exception:
            pass

    def test_create(self, uid):
        assert isinstance(uid, string_types)
        assert uid

    def test_list(self, session):
        num = 0
        for c in scgapi.Contact.Resource(session).list():
            num += 1
            break
        assert num > 0

    def test_get(self, session, uid, test_setup):
        contact = scgapi.Contact.Resource(session).get(uid)
        assert contact.id == uid
        assert contact.first_name == 'test'
        assert contact.primary_mdn == str(test_setup['mdnRangeStart'])

    def test_update(self, session, uid):
        contact = scgapi.Contact.Resource(session).get(uid)
        contact.first_name = 'Testing'
        contact.update()
        updated = scgapi.Contact.Resource(session).get(uid)
        assert updated.id == uid
        assert updated.first_name == 'Testing'

    def test_delete(self, session, uid):
        scgapi.Contact.Resource(session).delete(uid)

        with pytest.raises(scgapi.HttpRequestError):
            scgapi.Contact.Resource(session).get(uid)

