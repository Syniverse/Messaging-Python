from scgapi.Scg import Scg
import scgapi.MessageRequest
import scgapi.Contact
import scgapi.ContactGroup
import argparse

def send_sms(api, config, bob_mdn, alice_mdn, senderid):

    # Construct an instance of the authentication object
    # with authentication data from a json file (auth.json)
    auth = scgapi.AuthInfo(config=config)

    # Prepare a session to the server.
    scg = Scg()

    # Prepare a session to the server.
    session = scg.connect(auth, api)

    # Create some contacts
    contacts_res = scgapi.Contact.Resource(session)
    bob = contacts_res.create(first_name="Bob", primary_mdn=bob_mdn)
    alice = contacts_res.create(first_name="Alice", primary_mdn=alice_mdn)

    # Create a group
    grp_res = scgapi.ContactGroup.Resource(session)
    friends = grp_res.get(grp_res.create(name="Our Friends"))

    # add our new friends to the group
    friends.add_contact([bob, alice])

    # Get a MessageRequest resource
    mrq_res = scgapi.MessageRequest.Resource(session)

    # Send the message
    # Note that from_ has a padding underscore due to
    # syntax constraints in Python.
    reqid = mrq_res.create(
        from_=senderid,
        to=["group:" + friends.id],
        body="Hello, this is a SMS message to our friends.")

    print('Sent message request {} to group {}'.format(reqid, friends.id))

    # Clean up
    friends.delete()
    contacts_res.delete(bob)
    contacts_res.delete(alice)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('senderid', help='Sender-id to send from')
    parser.add_argument('bob', help='GSM number to send to')
    parser.add_argument('alice', help='GSM number to send to')
    parser.add_argument('--api', help='URL to the API server', default=None)
    parser.add_argument('--auth', help='Location of json auth file', default='auth.json')
    args = parser.parse_args()
    send_sms(api=args.api, config=args.auth, bob_mdn=args.bob, alice_mdn=args.alice, senderid=args.senderid)
