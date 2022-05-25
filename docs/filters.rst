.. currentmodule:: cion

Understanding Filters
=====================

A filter is a function that takes a value (the value is the the data being validated), performs an action on the data or verifies something, and then returns the value.

Here is a basic example of a filter:

.. code-block:: py

    def actual_filter_function(value):
        return value
    
    # in a field in a schema
    filters=[
        actual_filter_function # note that we don't call the function, since we want it to get called later when validating data
    ]

Now, knowing that all filters are are functions, we can create functions that create a customized function.
This is how Cion creates filters that aren't set to one value.

An example of a function that returns a filter:

.. code-blocK:: py

    def not_value(to_not_be: string):
        def filter(value: string):
            if value == to_not_be:
                raise ValidatorError(f"Must not be equal to {to_not_be}")

            return value
        return filter

    # we can then call ths multiple times, to check different things
    # now obviously this is inefficient and cion has a better way to do this through the not_one_of validator
    # but this is a simple example of how filters work

    # we can add it to a field like this
    filters=[
        not_value("admin"), # note that we call the function since the function returns the actual validator
        not_value("sphinx"),
        not_value("cion"),
    ]

If you are planning to make custom filters, please check out the :doc:`custom filters <custom_filters>` page.

Order
#####

The way that :func:`cion.Schema.validate` calls filters is in the exact order that they are specified.

It looks a little something similar to this:

.. code-block::

    for filter in field.filters:
        value = filter(value)

Putting filters that transform values in the wrong order might result in unexpected behavior.
Just make sure to read the documentation for the filters you are using and keep in mind the order of your filters.

Errors
######

When going through filters, if the filter raises a :class:`cion.exceptions.ValidatorError`, it is handled and added to the total errors in a :class:`cion.exceptions.ValidationError`.

Anything else is ignored. If a filter raises an error that isn't :class:`cion.exceptions.ValidatorError`, it will not be handled by :func:`cion.Schema.validate`

