from scgapi.Scg import Scg
import scgapi.SenderId
import argparse

def create_and_update_contact(api, config, mdn):
    # Construct an instance of the authentication object
    # with authentication data from a json file (auth.json)
    auth = scgapi.AuthInfo(config=config)

    # Prepare a session to the server.
    scg = Scg()

    # Prepare a session to the server.
    session = scg.connect(auth, api)

    res = res = scgapi.Contact.Resource(session)

    # Create a contact. Note that we get a contact id (string), not a Contact
    # instance from Create.
    contact_id = res.create(
        first_name="John",
        last_name="Doe",
        primary_mdn=mdn)

    contact = res.get(contact_id)
    contact.last_name = 'Anderson'
    contact.update()

    # Make sure we have same data as the server does
    updated_contact = res.get(contact_id)

    print("John Doe changed name to {} {}".format(updated_contact.first_name,
                                                  updated_contact.last_name))

    # Delete the contact on the server.
    contact.delete()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mdn', help='GSM number for the contact')
    parser.add_argument('--api', help='URL to the API server', default=None)
    parser.add_argument('--auth', help='Location of json auth file', default='auth.json')
    args = parser.parse_args()
    create_and_update_contact(api=args.api, config=args.auth, mdn=args.mdn)
