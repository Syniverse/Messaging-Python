from scgapi.Scg import Scg
import scgapi.MessageRequest
import argparse

def send_sms(api, config, mdn, senderid):
    # Construct an instance of the authentication object
    # with authentication data from a json file (auth.json)
    auth = scgapi.AuthInfo(config=config)

    # Prepare a session to the server.
    scg = Scg()

    # Prepare a session to the server.
    session = scg.connect(auth, api)

    # Get a MessageRequest resource
    res = scgapi.MessageRequest.Resource(session)

    # Send the message
    # Note that from_ has a padding underscore due to
    # syntax constraints in Python.
    reqid = res.create(
        from_=senderid,
        to=[mdn],
        body="Hello, this is a SMS message.")

    print('Sent message request {}'.format(reqid))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('senderid', help='Sender-id to send from')
    parser.add_argument('mdn', help='GSM number to send to')
    parser.add_argument('--api', help='URL to the API server', default=None)
    parser.add_argument('--auth', help='Location of json auth file', default='auth.json')
    args = parser.parse_args()
    send_sms(api=args.api, config=args.auth, mdn=args.mdn, senderid=args.senderid)
