===============
Getting Started
===============

Connecting to Mumble
====================

First you'll need to connect to the Mumble server's meta interface. To have write access you'll need to provide the ICE write secret defined in the ``murmur.ini``.

.. code-block:: python

    from mumble import Meta

    meta = Meta('ice-secret')

Selecing a Server instance
==========================

You'll need to select a server instance using the Meta interface. You can either get all the servers or select a specific one by Server ID.

.. code-block:: python

    servers = meta.get_all_servers()
    server = meta.get_server(1)

Full Example
============

.. code-block:: python

    from mumble import Meta

    meta = Meta()
    server = meta.get_server(1)

    print "Users"
    print "====="
    for user in server.get_users():
        print "* %s" % user.name
