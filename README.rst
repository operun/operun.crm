==========
operun CRM
==========

.. image:: https://travis-ci.org/operun/operun.crm.svg?branch=master
    :target: https://travis-ci.org/operun/operun.crm


Introduction
------------

operun CRM is a simple Plone based Customer-Relationship-Management (CRM) system.
It comes with basic Content-Types for Accounts, Contacts and Todos.

It contains the following:

* Account
* Contact
* Todo

This system is inspired by Zurmo. Use this package if other web-based CRMs like SugarCRM or similar are oversized for your requirements.


Compatibility
-------------

Version 1.0.0 is tested with Plone 4.3.x.
Version 1.0.0 is tested with Plone 5.0.x with a few exceptions:

* You must define the ``plone.formwidget.contenttree`` package inside your buildout.

.. code-block:: ini

    eggs =
        ...
        plone.formwidget.contenttree

* For Plone 5 it may be necessary to pin ``plone.formwidget.contenttree`` in your versions.

.. code-block:: ini

    plone.formwidget.contenttree = 1.0.15


Installation
------------

Add this line to the eggs section of your ``buildout.cfg``.

.. code:: ini

    eggs =
        ...
        operun.crm


Dependency Installation
-----------------------

If you want to add ``operun.crm`` as a dependency to another product, use the ``default`` profile in your ``metadata.xml``.

.. code:: xml

    <metadata>
      <version>1</version>
        <dependencies>
          ...
          <dependency>profile-operun.crm:default</dependency>
          ...
        </dependencies>
    </metadata>


Toubleshooting
--------------

Please report issues in the bugtracker at https://github.com/operun/operun.crm/issues.
