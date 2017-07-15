import os
import json
import pytest
import scgapi
from scgapi.Scg import Scg

@pytest.fixture(scope="session")
def test_setup():
    with open(os.environ['TEST_SETUP'], 'r') as f:
        return json.loads(f.read())

@pytest.fixture(scope="session")
def session():
    auth = scgapi.AuthInfo(config=os.environ['TEST_AUTH'])
    return Scg().connect(auth, test_setup()['url'])

