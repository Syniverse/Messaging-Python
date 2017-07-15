import pytest
import scgapi
import scgapi.ContactGroup
from six import string_types

class TestContactGroups():
    @pytest.fixture(scope="class")
    def cgid(self, session):
        contact_id = scgapi.ContactGroup.Resource(session).create(name='Friends')
        yield contact_id
        try:
            scgapi.ContactGroup.Resource(session).delete(contact_id)
        except Exception:
            pass

    @pytest.fixture(scope="class")
    def alice(self, session, test_setup):
        id = scgapi.Contact.Resource(session).create(
            first_name='alice', primary_mdn=str(test_setup['mdnRangeStart'] + 1))
        yield id
        try:
            scgapi.Contact.Resource(session).delete(id)
        except Exception:
            pass

    @pytest.fixture(scope="class")
    def bob(self, session, test_setup):
        id = scgapi.Contact.Resource(session).create(
            first_name='bob', primary_mdn=str(test_setup['mdnRangeStart'] + 2))
        yield id
        try:
            scgapi.Contact.Resource(session).delete(id)
        except Exception:
            pass

    def test_create(self, cgid):
        assert isinstance(cgid, string_types)
        assert cgid

    def test_list(self, session):
        num = 0
        for c in scgapi.ContactGroup.Resource(session).list():
            num += 1
            break
        assert num > 0

    def test_get(self, session, cgid, test_setup):
        cg = scgapi.ContactGroup.Resource(session).get(cgid)
        assert cg.id == cgid
        assert cg.name == 'Friends'

    def test_contacts(self, session, cgid, alice, bob):
        friends = scgapi.ContactGroup.Resource(session).get(cgid)
        friends.add_contact([bob, alice])
        friend_contacts = list(friends.list_contacts())
        assert friend_contacts
        assert len(friend_contacts) == 2

    def test_delete(self, session, cgid):
        scgapi.ContactGroup.Resource(session).delete(cgid)

        with pytest.raises(scgapi.HttpRequestError):
            scgapi.ContactGroup.Resource(session).get(cgid)

