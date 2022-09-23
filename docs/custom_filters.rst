.. currentmodule:: cion

Creating Custom Filters
=======================

While Cion comes with a rich built in set of filters that can convert values, enforce types, and validate items, it is probable that you will want to create your own custom filter for a specialized use case.

Tutorial
########

All the code for this is found in `examples/custom_filter.py <https://github.com/meizuflux/cion/blob/master/examples/custom_filter.py>`_

First, we want to create our custom filter function. For this example, we will create a validator that ensures that a list of integers is in order.

First, we need to make sure that the value passed is something that we can iterate through. Make sure to add ``from typing import Iterable`` at the top of your file.

.. literalinclude:: ../examples/custom_filter.py
    :pyobject: numbers_in_order
    :lines: 1-3
    :emphasize-lines: 2

After that, we need to go and ensure that the list is in the proper order.
As we go through the list, we need to make sure that the item we are currently comparing is an ``int``.
Then, we ignore the first item, since comparing it with the item behind it would use the last item in the list, which is not what we want.
So, after we check that it isn't the first item, we check that it is larger than the item behind it. If it is, we raise an error.

.. literalinclude:: ../examples/custom_filter.py
    :pyobject: numbers_in_order
    :lines: 5-13
    :emphasize-lines: 4, 7-8

From there, we can assign the filter to a field in a schema.

.. literalinclude:: ../examples/custom_filter.py
    :start-after: # [Schema Start]
    :end-before: # [Schema End]
    :emphasize-lines: 4-5

Once we have declared a schema, we can validate any data.

.. literalinclude:: ../examples/custom_filter.py
    :start-after: # [Start OK]
    :end-before: # [End OK]
    :caption: Passes

.. literalinclude:: ../examples/custom_filter.py
    :start-after: # [Start Fails: list]
    :end-before: # [End Fails: list]
    :caption: Fails, it must be a list

.. literalinclude:: ../examples/custom_filter.py
    :start-after: # [Start Fails: int]
    :end-before: # [End Fails: int]
    :caption: Fails, it must be a list of integers

.. literalinclude:: ../examples/custom_filter.py
    :start-after: # [Start Fails: order]
    :end-before: # [End Fails: order]
    :caption: Fails, the list must be in order







