===============
Getting Started
===============

------------
Installation
------------

You can install nova-trame directly with

.. code-block:: bash

    pip install nova-trame

or with `Pixi <https://pixi.sh/latest/>`_ with:

.. code-block:: bash

    pixi add --pypi nova-trame

-----------------------
Creating an Application
-----------------------

To create your application, you'll first need to setup an application class that inherits from :code:`nova.trame.TrameApp`. This class will provide a default layout and theme for your application.

.. literalinclude:: ../tests/test_theme.py
    :start-after: setup app
    :end-before: setup app complete
    :dedent:

Now you can run your application with the following:

.. literalinclude:: ../tests/gallery/main.py
    :start-after: run app
    :end-before: run app complete
    :dedent:

If you installed via Pixi, you can run the above script with:

.. code-block:: bash

    pixi run python my_trame_app.py [--server]

After running this, if you point your browser to http://localhost:8080, then you should see a basic web application with our default theme and a button that says "Hello World".

The optional :code:`--server` argument is passed to the Trame server and will prevent Trame from opening a new browser tab on launch.

By default your application will shut itself down one hour after the last client disconnects (or one hour after startup if nobody ever connects). See :code:`ThemedApp.client_disconnect_timeout` and :code:`ThemedApp.on_client_disconnected` if you need to change the timeout or what happens when it elapses.
