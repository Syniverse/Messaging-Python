# Python SDK for SCG Messaging APIs

This is the Python version of the SCG API.
We have prepared simple to use Python classes, representing the
different REST API interfaces.

The Python API hides some of the REST API's constraints, like
lists being returned in logical pages of <i>n</i> records. With the
python SDK, the list() method returns a generator that returns
single list items, util there are no more.

The SDK is compatible with Python 2.7 and 3.5

## How to use the SDK
All the data objects follow a common pattern.

You get a handle to a resource (like Contact or SenderId) by getting
an instance of scgapi.Object.Resource(session).

The session object is obtained from Scg.connect(), and gives you
sequential (blocking) access to the REST API. If you want to
process many requests in parallel, you need many session objects.
Python has some architectural constrains on true multiprocessing,
but as REST requests typically waits on the server for quite some
time (measured in milliseconds or even seconds), you can achieve
quite some extra performance from using a large number of sessions.

The resource object you get from  scgapi.<Object>.Resource(session)
typically has <b>list()</b> and <b>create()</b> methods (depending
on the actual REST API methods available for that data type).

To list the data objects for a resource, like your Contacts,
you can call list() without any arguments to get all the contacts,
or list(key=value[, key=value]...) to filter the result-set. list()
returns a generator that let's you iterate over the data-set.

You can create an object by calling create() with name=value pairs,
or by constructing and initializing a data object, and then passing
it to create().

```python
# Create from name/value pairs
res = scgapi.Contact.Resource(session)
id = create(first_name="John", last_name="Doe")
```

```python
# Create from object
res = scgapi.Contact.Resource(session)
contact = scgapi.Contact()
contact.first_name="John"
contact.last_name="Doe"
id = create(contact)
```

All objects that can be updated or deleted has <b>update()</b> and/or
<b>delete()</b> methods. The resource of an object also have <b>delete()</b>
methods, so if you need to delete an object you just know by it's id,
there is no need to instantiate it. You jst call
 ```python
res.delete(id)
```

Some objects has methods that let you add/query or delete
other objects or references it holds to other objects. For
example, when you create a message-request to a group of
contacts, you may generate a large number of message objects.
These can be iterated over from scgapi.MessageRequest.list_messages()

```python
res = mrq_res = scgapi.MessageRequest.Resource(session)
request = mrq_res.get("qteDxVrAhlMlmTwDrMAvN3")
for msg in request.list_messages():
    # Do something...
```

## Error handling
Errors are reported trough exceptions.

## Special considerations
The REST API has some read-only
properties for some objects (like the server-generated id). These
are retained as read-only in this SDK. In the source code, the
read-only properties are hidden with a prefix underscore and
accessed trough Python reader properties. So even if the 'id' of
all objects are read-only, you can still get the value by accessing
'instance.id'. The same applies for other read-only properties.

Python have some reserved words that cannot be used as an argument name.
In this SDK, we have solved this by allowing a padding underscore
on all argument names that represents an object property.

For example, if we want to create an object that has a property name 
of 'from', and set that property value, we can write:
```python
res.create(foo="Foo", from_="Me")
```
The same applies for filters in the list() methods.
```python
res.list(foo="Foo", from_="Me")
```

# Some examples

## Listing Sender Ids
If you want to list available Sender Ids, it can be done as easy as:
```python
def list_senderids(api, config):
    # Construct an instance of the authentication object
    # with authentication data from a json file (auth.json)
    auth = scgapi.AuthInfo(config=config)

    # Prepare a session to the server.
    scg = Scg()

    # Prepare a session to the server.
    session = scg.connect(api, auth)

    # Request the complete list of sender id's from the server,
    # where the class_id is COMMECRIAL and state is ACTIVE, and iterate
    # over them one by one.
    res = scgapi.SenderId.Resource(session)
    for sid in res.list(class_id="COMMERCIAL", state="ACTIVE"):
        print('Sender id {} has capabilities {}'.format(sid.address,
                                                        sid.capabilities))
```
[Full example](examples/list_senderids.py)

This should produce output like:
```text
Sender id +15552223561 has capabilities ['VOICE']
Sender id +15552460009 has capabilities ['VOICE']
Sender id 15555551122 has capabilities ['SMS']
Sender id 155528999 has capabilities ['MMS', 'SMS']
```


## Adding and updating a Contact
```python
def create_and_update_contact(api, config, mdn):
    # Construct an instance of the authentication object
    # with authentication data from a json file (auth.json)
    auth = scgapi.AuthInfo(config=config)

    # Prepare a session to the server.
    scg = Scg()

    # Prepare a session to the server.
    session = scg.connect(api, auth)

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
```
[Full example](examples/update_contact.py)

This should produce output similar to:
```text
John Doe changed name to John Anderson
```

## Sending a SMS to a Mobile number
```python
def send_sms(api, config, mdn, senderid):
    # Construct an instance of the authentication object
    # with authentication data from a json file (auth.json)
    auth = scgapi.AuthInfo(config=config)

    # Prepare a session to the server.
    scg = Scg()

    # Prepare a session to the server.
    session = scg.connect(api, auth)

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

```
[Full example](examples/send_sms.py)

This should produce output similar to:
```text
Sent message request aQWY9PeMCO01TEH9bk1ek5
```

## Sending a Message to a Contact

This works as above, except for the to field in create()
```python
contact_id = "<Id of an existing contact>"
reqid = mrq_res.create(
    from_=sender_id,
    to=["contact:" + contact_id],
    body="Hello, this is a SMS message.")
```

## Sending a Message to a Contact Group
```python
def send_sms(api, config, bob_mdn, alice_mdn, senderid):

    # Construct an instance of the authentication object
    # with authentication data from a json file (auth.json)
    auth = scgapi.AuthInfo(config=config)

    # Prepare a session to the server.
    scg = Scg()

    # Prepare a session to the server.
    session = scg.connect(api, auth)

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
```
[Full example](examples/send_sms_to_grp.py)


## Sending a MMS with an attachment

```python
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
    session = scg.connect(api, auth)

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
```
```text
Uploaded attachment wMjURamVl9ITSXRJSkMoR4
Sent message request 9NeqCbNXBYvRO73jC2rbc5
```
[Full example](examples/send_mms.py)


## Checking the state of a Message Request
```python
def check_state(api, config, mrq):

    # Construct an instance of the authentication object
    # with authentication data from a json file (auth.json)
    auth = scgapi.AuthInfo(config=config)

    # Prepare a session to the server.
    scg = Scg()

    # Prepare a session to the server.
    session = scg.connect(auth, api)

    # Get a MessageRequest resource
    res = scgapi.MessageRequest.Resource(session)

    # Get the message request instance
    message_request = res.get(mrq)

    print('Message Request {} is in state {} with {} delivered and {} failed messages'.format(
        message_request.id,
        message_request.state,
        message_request.delivered_count,
        message_request.failed_count))

    # Get a generator to the messages generated by this message request
    msgs = message_request.list_messages()

    # Print each message.
    #
    # Since the SDK use a generator and not a list, we will only have a small
    # number of messages in memory at any time, allowing us to iterate
    # over many messages if required, even on machines with very
    # limited internal memory.
    for msg in msgs:
        print(' - Message {} is in state {}, error code: {}, error reason: {}'.format(
            msg.id, msg.state, msg.failure_code, msg.failure_details))
        for frag in msg.fragments_info:
            print ('   - Fragment {} has state {}'.format(frag.fragment_id, frag.fragment_state))
```
[Full example](examples/check_message_request_state.py)

This should produce output similar to:
```text
Message Request mjwLKqumB82wGAU8kwv317 is in state COMPLETED with 0 delivered and 0 failed messages
 - Message TXgPr187zLzUAWYEorHmU2 is in state SENT, error code: None, error reason: None
   - Fragment A87UrgwRiK0QnjDM3AMEv2 has state SENT

```

# Using with virtualenv

In order to use the library in a private environment,
without creating conflicts with other Python packages,
you can use virtualenv. The example below is tested with
Ubuntu zesty.

```bash
$ virtualenv -p /usr/bin/python3 env-p3
$ . ./env-p3/bin/activate
$ pip install -r requirements.txt
$ python examples/list_senderids.py 
```

