from scgapi.Scg import Scg
import scgapi.SenderId
import argparse

def list_senderids(api, config):
    # Construct an instance of the authentication object
    # with authentication data from a json file (auth.json)
    auth = scgapi.AuthInfo(config=config)

    # Prepare a session to the server.
    scg = Scg()

    # Prepare a session to the server.
    session = scg.connect(auth, api)

    # Request the complete list of sender id's from the server,
    # where the class_id is COMMECRIAL and state is ACTIVE, and iterate
    # over them one by one.
    res = scgapi.SenderId.Resource(session)
    for sid in res.list(class_id="COMMERCIAL", state="ACTIVE"):
        print('Sender id {} has capabilities {}'.format(sid.address,
                                                        sid.capabilities))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--api', help='URL to the API server', default=None)
    parser.add_argument('--auth', help='Location of json auth file', default='auth.json')
    args = parser.parse_args()
    list_senderids(api=args.api, config=args.auth)
