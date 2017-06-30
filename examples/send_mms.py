from scgapi.Scg import Scg
import scgapi.MessageRequest
import argparse

def upload_attachment(session, path):
    res = scgapi.Attachment.Resource(session)
    att = res.create_and_upload(path, type="image/jpeg",
        name="attachment", filename="attachment.jpg")
    print('Uploaded attachment {}'.format(att.id))
    return att

def send_mms(api, config, mdn, senderid, attachment):
    # Construct an instance of the authentication object
    # with authentication data from a json file (auth.json)
    auth = scgapi.AuthInfo(config=config)

    # Prepare a session to the server.
    scg = Scg()

    # Prepare a session to the server.
    session = scg.connect(auth, api)

    # Get a MessageRequest resource
    res = scgapi.MessageRequest.Resource(session)

    # Upload the attachment to the server.
    # Returns an instance of scgapi.Attachment
    att = upload_attachment(session, attachment)

    # Send the message
    # Note that from_ has a padding underscore due to
    # syntax constraints in Python.
    reqid = res.create(
        from_=senderid,
        to=[mdn],
        attachments=[att.id],
        body="Hello, this is a MMS message.")

    print('Sent message request {}'.format(reqid))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('senderid', help='Sender-id to send from')
    parser.add_argument('mdn', help='GSM number to send to')
    parser.add_argument('attachment', help='Path to attachment (jpeg picture)')
    parser.add_argument('--api', help='URL to the API server', default=None)
    parser.add_argument('--auth', help='Location of json auth file', default='auth.json')
    args = parser.parse_args()
    send_mms(api=args.api, config=args.auth, mdn=args.mdn,
             senderid=args.senderid, attachment=args.attachment)
