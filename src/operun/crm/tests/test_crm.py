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

        # Create Contact
        self._create_contact(contacts_obj)
        view = contacts_obj.restrictedTraverse('view')
        output = view()
        self.assertTrue(output)
        self.assertIn('Max Mustermann' and 'Mary Lee', output)

        # Check Contacts Modify
        self.assertEqual(contacts_obj.description, u'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.')  # noqa
        contacts_obj.description = RichTextValue(
            u'ι ℓσνє ρℓσиє! Plone 5 2017',
            'text/plain',
            'text/html'
        )
        contacts_obj.reindexObject()
        self.assertTrue(output)
        self.assertEqual(contacts_obj.description.raw, u'\u03b9 \u2113\u03c3\u03bd\u0454 \u03c1\u2113\u03c3\u0438\u0454! Plone 5 2017')  # noqa

    def test_contact(self):
        contacts_folder = api.content.find(portal_type='Contacts')
        contact_items = api.content.find(portal_type='Contact')
        contacts = contacts_folder[0]
        contact = contact_items[0]
        contacts_obj = contacts.getObject()
        contact_obj = contact.getObject()

        # Check Demo Title
        self.assertEqual(contact_obj.title, 'Max Mustermann')

        # View Contact
        view = contact_obj.restrictedTraverse('view')
        output = view()
        self.assertTrue(output)
        self.assertIn('max.mustermann@musterfirma.de', output)

        # Check Contact
        new_contact = self._create_contact(contacts_obj)
        view = new_contact.restrictedTraverse('view')
        output = view()
        self.assertTrue(output)
        self.assertEqual(new_contact.notes.raw, u'\u03b9 \u2113\u03c3\u03bd\u0454 \u03c1\u2113\u03c3\u0438\u0454! Plone 5 2017')  # noqa

        # Check Length of Contacts
        contact_items = api.content.find(portal_type='Contact')
        self.assertEqual(len(contact_items), 2)

        # Check Contact Modify
        self.assertEqual(new_contact.phone, '+49 8070 4546 700')
        new_contact.phone = '+49 8070 4546 705'
        new_contact.reindexObject()
        self.assertEqual(new_contact.phone, '+49 8070 4546 705')
