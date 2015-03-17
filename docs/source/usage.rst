Usage
=====

DictRemapper
------------

This class can remap a dictionary if a keymap is passed as argument.

.. code-block:: python

    import redict

    keymap = {
        'message': 'm',
        'user': 'u',
        'permissions': 'p',
        'role': 'r',
    }

    data = {
        'message': 'hello world',
        'user': 1,
        'permissions': [
            {'role': 1, },
            {'role': 2, },
            {'role': 3, },
        ]
    }

    remapped = redict.DictRemapper(data, keymap=keymap)()

Results in:
::

    {
        'm': 'hello world',
        'u': 1,
        'p': [
            {'r': 1, },
            {'r': 2, },
            {'r': 3, },
        ]
    }


.. note::
    Currently using integers as dict keys are not supported.


JsonRemapper
------------

This class can remap a json string if a keymap is passed as argument.
In case you're working with big json files, it can help to reduce the size of your json files.

.. code-block:: python

    import redict

    keymap = {
        'message': 'm',
        'user': 'u',
        'permissions': 'p',
        'role': 'r',
    }

    json_string = (
        '{"message": "hello world", "user": 1, '
        '"permissions": [{"role": 1, }, {"role": 2, }, {"role": 3, }]}'
    )

    remapped = redict.JsonRemapper(json_string, keymap=keymap)()

Results in:
::

    '{"m": "hello world", "u": 1, "p": [{"r": 1, }, {"r": 2, }, {"r": 3, },]}'


You can also minify the result:

.. code-block:: python

    remapped = redict.JsonRemapper(json_string, keymap=keymap, minify=True)()

::

    '{"m":"helloworld","u":1,"p":[{"r":1,},{"r":2,},{"r":3,},]}'
