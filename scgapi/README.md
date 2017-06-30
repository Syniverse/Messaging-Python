# scgapi Module

This is the source code for the scgapi SDK module.

The sdk has a generic architecture, taking advantage of Pythons
dynamic class definition. The attributes for the different objects
are defined in a _get_member_variable_names(self) method. To
understand what arguments that are available, please look at
the ones defined there. For example, the Channel class
contains these attributes:
```python
    def _get_member_variable_names(self):
        return ("_id", "name", "priority", "role",
                "description", "_ownership", "_application_id",
                "_created_date", "_last_update_date",
                "_version_number")
```
The ones starting with underscore are read-only and will not be
sent to the server if update() is called. They can still be
read from the object without the underscore.
```python
res = scgapi.Channel.Resource(session)
channel = res.get("<some valid channel id>")
print('we got channel id {} with ownership {}'.format(channel.id, channel.ownership)
```

The SDK classes are documented with python docstrings.

