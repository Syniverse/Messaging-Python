from scgapi.Scg import Scg
import scgapi.SenderId
import argparse

def process(api, config, args):
    # Construct an instance of the authentication object
    # with authentication data from a json file (auth.json)
    auth = scgapi.AuthInfo(config=config)

    # Prepare a session to the server.
    scg = Scg()

    # Prepare a session to the server.
    session = scg.connect(auth, api)
    res = scgapi.SenderId.Resource(session)

    # Initialize whatsapp setup
    if args.phone_number and args.token:
        reqid = res.create(name="sender-wa-" + args.phone_number,
                           capabilities=["WHATSAPP"],
                           class_id="COMMERCIAL",
                           type_id="WHATSAPP",
                           address=args.phone_number,
                           ownership="PRIVATE",
                           credentials='{"token": "' + args.token + '"}'
        )

        print('Created sender-id {} '.format(reqid))

    # Initialize whatsapp setup
    if args.register_method and args.sender_id:
        si = res.get(args.sender_id)
        si.init_whatsapp_registration(args.register_method)

    # Activate whatsapp using code received by the step above
    if args.verification_code and args.sender_id:
        si = res.get(args.sender_id)
        si.activate_whatsapp_registration(args.verification_code)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--api', help='URL to the API server', default=None)
    parser.add_argument('--auth', help='Location of json auth file', default='auth.json')
    parser.add_argument('--verification-code', help='Verification code from whatsapp', default=None)
    parser.add_argument('--register-method', help='sms or voice - used to initialize registration with whatsapp', default=None)
    parser.add_argument('--phone-number', help='Create a whatsapp senderid using this number', default=None)
    parser.add_argument('--token', help='Token needed to create whatsapp sender-id', default=None)
    parser.add_argument('--sender-id', help='Sneder-id for provisioning', default=None)
    args = parser.parse_args()
    process(api=args.api, config=args.auth, args=args)
