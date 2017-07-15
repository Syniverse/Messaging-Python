
import os
import pytest
import scgapi
import scgapi.Attachment
from six import string_types

class TestAttachments():
    @pytest.fixture(scope="class")
    def aid(self, session):
        att_id = scgapi.Attachment.Resource(session).create(
            name='test_upload', type='image/jpeg', 
            filename='cutecat.jpg')
        yield att_id
        try:
            scgapi.Attachment.Resource(session).delete(att_id)
        except Exception:
            pass

    def test_create(self, aid):
        assert isinstance(aid, string_types)
        assert aid

    def test_list(self, session):
        num = 0
        for c in scgapi.Attachment.Resource(session).list():
            num += 1
            break
        assert num > 0

    def test_get(self, session, aid):
        attachment = scgapi.Attachment.Resource(session).get(aid)
        assert attachment.id == aid
        assert attachment.size is None or attachment.size == 0
        assert attachment.state == 'CREATED'
        
    def test_upload(self, session, aid):
        up_name = 'tmp.attfile.jpg'
        with open(up_name, 'w') as f:
            f.write('Test data')

        attachment = scgapi.Attachment.Resource(session).get(aid)
        attachment.upload(up_name)
        os.remove(up_name)

        attachment = scgapi.Attachment.Resource(session).get(aid)
        assert attachment.size > 0
        assert attachment.state == 'UPLOADED'

    def test_create_and_upload(self, session):
        up_name = 'tmp.attfile.jpg'
        with open(up_name, 'w') as f:
            f.write('Test data')

        attachment = scgapi.Attachment.Resource(session).create_and_upload(
            up_name, name="testattachment", filename="test.jpg")

        os.remove(up_name)

        assert attachment.size > 0
        assert attachment.state == 'UPLOADED'
        try:
            attachment.delete()
        except:
            pass


    def test_delete(self, session, aid):
        scgapi.Attachment.Resource(session).delete(aid)

        with pytest.raises(scgapi.HttpRequestError):
            scgapi.Attachment.Resource(session).get(aid)

