Introduction
============

operun.crm is a simple Plone based Customer-Relationship-Management (CRM) system. It comes with basic Content-Types for Accounts and Contacts.

It contains the following:

* Account
* Contact
* Todo

This system is inspired by Zurmo. Use this package if other web-based CRMs like SugarCRM or similar are oversized for your requirements.


Compatibility
=============

Version 1.0.0 is tested with Plone 4.3.x & 5.0.x.


Installation
============

Add this line in the eggs section of your ``buildout.cfg``

.. code:: ini

    eggs =
        ...
        operun.crm


Installation as a dependency
-------------------------------------------------

If you want to add ``operun.crm`` as a dependency to another product, use the ``default`` profile in your ``metadata.xml``.

.. code:: xml

    <metadata>
      <version>1</version>
        <dependencies>
            <dependency>profile-operun.crm:default</dependency>
        </dependencies>
    </metadata>


Toubleshooting
==============

Please report issues in the bugtracker at https://github.com/operun/operun.crm/issues.


Branches
========

The master-branch supports Plone 4 & 5 only.


License
=======

GNU General Public License, version 2


Contributors
============

* Stefan Antonelli <stefan.antonelli@operun.de>
* Jesse Stippel <jesse.stippel@operun.de>
