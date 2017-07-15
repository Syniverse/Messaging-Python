import scgapi
import scgapi.ContactAddressHistory

class TestContactAddressHistory():

    def test_list(self, session):
        num = 0
        for c in scgapi.ContactAddressHistory.Resource(session).list():
            num += 1
            break
        assert num > 0

