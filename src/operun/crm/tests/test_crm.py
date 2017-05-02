# -*- coding: utf-8 -*-

from operun.crm.testing import OPERUN_CRM_INTEGRATION_TESTING
from plone import api
from plone.app.testing import login
from plone.app.testing import SITE_OWNER_NAME
from plone.app.textfield.value import RichTextValue

import unittest2 as unittest


class TestCrm(unittest.TestCase):
    """Tests for the operun.crm project."""

    layer = OPERUN_CRM_INTEGRATION_TESTING

    def _create_contacts(self):
        return api.content.create(
            container=self.portal,
            type='Contacts',
            title='Contacts',
            id='contacts',
            text=RichTextValue(u'ι ℓσνє ρℓσиє! Plone 5 2017',
                               'text/plain',
                               'text/html'),
        )

    def _create_contact(self, container):
        return api.content.create(
            container=container,
            type='Contact',
            title='Mary Lee',
            id='mary-lee',
            text=RichTextValue(u'ι ℓσνє ρℓσиє! Plone 5 2017',
                               'text/plain',
                               'text/html'),
            firstname='Mary',
            lastname='Lee',
            account='customer',
            phone='+49 8070 4546 700',
            mobile='+49 172 8030 100',
            email='mary.lee@example.de',
            notes=RichTextValue(u'ι ℓσνє ρℓσиє! Plone 5 2017',
                                'text/plain',
                                'text/html'),
        )

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        login(self.portal, SITE_OWNER_NAME)

    def test_contacts(self):
        contacts = self._create_contacts()
        contact = self._create_contact(contacts)

        self.assertEqual(contacts.title, 'Contacts', msg=None)
        self.assertEqual(contact.title, 'Mary Lee', msg=None)
