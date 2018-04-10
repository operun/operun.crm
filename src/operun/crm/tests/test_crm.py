# -*- coding: utf-8 -*-

from operun.crm.testing import OPERUN_CRM_INTEGRATION_TESTING
from plone import api
from plone.app.testing import login
from plone.app.testing import SITE_OWNER_NAME
from plone.app.textfield.value import RichTextValue

import unittest


class TestCrm(unittest.TestCase):
    """Tests for the operun.crm project."""

    layer = OPERUN_CRM_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        login(self.portal, SITE_OWNER_NAME)

    def test_contacts(self):
        contacts_folder = api.content.find(portal_type='Contacts')
        contacts = contacts_folder[0]
        contacts_obj = contacts.getObject()

        # Check Demo Title
        self.assertEqual(contacts_obj.title, 'Kontakte')

        # View Contacts
        view = contacts_obj.restrictedTraverse('view')
        output = view()
        self.assertTrue(output)
        self.assertIn('Max Mustermann', output)

        # Check Contacts Modify
        self.assertEqual(
            contacts_obj.description,
            'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, '
            'sed diam nonumy eirmod tempor invidunt ut labore et dolore '
            'magna aliquyam erat, sed diam voluptua. At vero eos et accusam '
            'et justo duo dolores et ea rebum. Stet clita kasd gubergren, no '
            'sea takimata sanctus est Lorem ipsum dolor sit amet.',
        )
        contacts_obj.description = RichTextValue(
            u'ι ℓσνє ρℓσиє! Plone 5 2017',
            'text/plain',
            'text/html'
        )
        contacts_obj.reindexObject()
        self.assertTrue(output)
        self.assertEqual(contacts_obj.description.raw, u'\u03b9 \u2113\u03c3\u03bd\u0454 \u03c1\u2113\u03c3\u0438\u0454! Plone 5 2017')  # noqa

    def test_contact(self):
        contact_items = api.content.find(portal_type='Contact')
        contact = contact_items[0]
        contact_obj = contact.getObject()

        # Check Demo Title
        self.assertEqual(contact_obj.title, 'Max Mustermann')

        # View Contact
        view = contact_obj.restrictedTraverse('view')
        output = view()
        self.assertTrue(output)
        self.assertIn('max.mustermann@musterfirma.de', output)

        # Check Length of Contacts
        contact_items = api.content.find(portal_type='Contact')
        self.assertEqual(len(contact_items), 1)
