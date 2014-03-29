Introduction
============

operun.crm is a simple Plone based Customer-Relationship-Management (CRM) System. It comes with basic content types for Accounts and Contacts.  

It contains the following types:

* Account
* Contact
* Todo

This System is inspired by Zurmo. Use this package if other web-based systems like SugarCRM or similar are oversiced for your requirements.
 

Compatibility
=============

Version 1.0.0 is tested with Plone 4.3.x.


Installation
============

Add this line in the eggs section of your ``buildout.cfg``

.. code:: ini

    eggs =
        ...
        operun.crm


Uninstalling
------------

TBD.


Dependencies
------------

* ``plone.app.dexterity >= 2.0.7``. Dexterity is shipped with Plone 4.3.x. Version pinns for Dexterity are included in Plone 4.2.x. For Plone 4.1.x you need to pin the correct version for Dexterity in your buildout. See `Installing Dexterity on older versions of Plone <http://developer.plone.org/reference_manuals/external/plone.app.dexterity/install.html#installing-dexterity-on-older-versions-of-plone>`_.

* ``plone.dexterity >= 2.2.1``. Olders version of plone.dexterity break the rss-views because plone.app.contenttypes uses behaviors for the richtext-fields.


Installation as a dependency from another product
-------------------------------------------------

If you want to add operun.crm as a dependency from another products use the profile ``default`` in your ``metadata.xml``.

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

The master-branch supports Plone 4 only.


License
=======

GNU General Public License, version 2


Contributors
============

* Stefan Antonelli <stefan.antonelli@operun.de>