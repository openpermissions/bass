************************************************
The Open Permissions Platform - Identity Library
************************************************

.. contents:: :depth: 1

Introduction
============

This is a Python library used for creating unique **hub keys** used
within the Open Permissions Platform.

`Click here for the Open Permissions Platform home
page <http://www.openpermissions.org/>`__

Dependencies
============

This has been tested using

-  Ubuntu 14.0.4
-  Python 2.7.10

Running tests
=============

Setup
-----

Prior to running any test the python pip dependencies need to be
installed. Run the following command to do this

.. code:: bash

    make requirements

Unit tests
----------

To run the unit tests run the following command

.. code:: bash

    make test

Logs will be found at tests/unit/reports

Behave tests
------------

To run the behave tests run the following command

.. code:: bash

    make behave

Logs will be found at tests/behave/reports

Documentation
-------------

To generate documentation, run the following command:

.. code:: bash

    make docs

Installation
============

::

    python setup.py install

Generate a hub key
==================

Code
----

.. code:: Python

    from bass.hubkey import create_hub_key

    hub_key = generate_hub_key(
        resolver_id='openpermissions.org',
        hub_id='hub1',
        repository_id='f8e3968eb99f48d6b9f84340efb64d47',
        entity_type="asset"
    )

    print hub_key

Output
------

.. code:: Console

    https://openpermissions.org/s1/hub1/f8e3968eb99f48d6b9f84340efb64d47/asset/79fa0ce2e082467cad24703dcfdf7317

Documentation
=============

Additional code documentation can be found at
http://bass.readthedocs.org/en/stable/
