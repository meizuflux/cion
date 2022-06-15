Getting started with Cion
=========================

Create a venv however you prefer, and then install cion from pip. 

.. code-block:: sh

    pip install cion

Then you can use it anywhere in your code.

.. code-block::
    
    import cion

    LoginSchema = cion.Schema(
        fields={
            "username": cion.Field(
                filters=[
                    cion.types.string(),
                    cion.validators.length(3, 64)
                ],
                required=True
            ),
            "password": cion.Field(
                filters=[
                    cion.types.string(),
                    cion.validators.length(3, 1024)
                ],
                required=True
            )
        }
    )

    LoginSchema.validate({
        "username": "meizuflux",
        "password": "password"
    })

First, we can create a Schema

.. code-block:: 

    import cion

    LoginSchema = cion.Schema()

Next, we add fields.

.. code-block::

    LoginSchema = cion.Schema(
        fields={
            "username": cion.Field(),
            "password": cion.Field()
        }
    )

After we have our fields, we can define filters. Filters are just functions that take the value and do something with it.
For instance, :func:`cion.validators.length` validates the length of the value.

.. code-block::

    LoginSchema = cion.Schema(
        fields={
            "username": cion.Field(
                filters=[
                    cion.types.string(),
                    cion.validators.length(3, 64)
                ],
                required=True
            ),
            "password": cion.Field(
                filters=[
                    cion.types.string(),
                    cion.validators.length(3, 1024)
                ],
                required=True
            )
        }
    )

Finally, after we have defined our schema, we can validate some data.

.. code-block:: 

    LoginSchema.validate({
        "username": "meizuflux",
        "password": "password"
    })

    # this works, as the values go through all of the filters without raising an error

.. code-block::

    LoginSchema.validate({
        "username": "m",
        "password": "password"
    })

    # this raises an error, as the username must be at least 3 characters in length

Read on in the rest of the documentation to learn how :exception:`cion.ValidationError` works, how filters work, and how to build and extend onto cion.

Full code.

.. code-block::
    
    import cion

    LoginSchema = cion.Schema(
        fields={
            "username": cion.Field(
                filters=[
                    cion.types.string(),
                    cion.validators.length(3, 64)
                ],
                required=True
            ),
            "password": cion.Field(
                filters=[
                    cion.types.string(),
                    cion.validators.length(3, 1024)
                ],
                required=True
            )
        }
    )

    LoginSchema.validate({
        "username": "meizuflux",
        "password": "password"
    })