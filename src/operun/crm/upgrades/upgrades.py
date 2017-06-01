# -*- coding: utf-8 -*-
"""
Migration steps for operun CRM.
"""
from operun.crm.content.account import Account
from operun.crm.content.accounts import Accounts
from operun.crm.content.contact import Contact
from operun.crm.content.contacts import Contacts
from operun.crm.content.invoice import Invoice
from operun.crm.content.offer import Offer
from operun.crm.content.todo import Todo
from operun.crm.content.todos import Todos
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.interface import alsoProvides
from zope.intid.interfaces import IIntIds
from transaction import commit


import logging


default_profile = 'profile-operun.crm:default'
logger = logging.getLogger('Plone')

content_type_mapping = {
    'operun.crm.account': 'Account',
    'operun.crm.accounts': 'Accounts',
    'operun.crm.contact': 'Contact',
    'operun.crm.contacts': 'Contacts',
    'operun.crm.invoice': 'Invoice',
    'operun.crm.offer': 'Offer',
    'operun.crm.todo': 'Todo',
    'operun.crm.todos': 'Todos',
}

content_type_classes = {
    'Account': Account,
    'Accounts': Accounts,
    'Contact': Contact,
    'Contacts': Contacts,
    'Invoice': Invoice,
    'Offer': Offer,
    'Todo': Todo,
    'Todos': Todos,
}


class MigrationsView(BrowserView):

    template = ViewPageTemplateFile('templates/upgrades.pt')

    def __call__(self):
        if self.request.form.get('form.buttons.update-attribute-assignment'):
            alsoProvides(self.request, IDisableCSRFProtection)
            self.update_attribute_assignment()
        if self.request.form.get('form.buttons.update-content-types'):
            alsoProvides(self.request, IDisableCSRFProtection)
            self.update_content_types()
        if self.request.form.get('form.buttons.update-displayed-types'):
            alsoProvides(self.request, IDisableCSRFProtection)
            self.update_displayed_types()
        if self.request.form.get('form.buttons.rebuild-and-clean'):
            alsoProvides(self.request, IDisableCSRFProtection)
            self.rebuild_and_clean()
        else:
            return self.template()

    def update_classes(self):
        """
        Updated the file definitions for objects
        """
        for content_type in content_type_classes:
            results = api.content.find(portal_type=content_type)
            content_type_class = content_type_classes[content_type]
            if results:
                logger.info('ASSIGNING {0} TO {1}'.format(content_type, content_type_class))  # noqa
                for item in results:
                    obj = item.getObject()
                    obj_id = obj.getId()
                    parent = obj.__parent__
                    obj.__class__ = content_type_class
                    parent._delOb(obj_id)
                    parent._setOb(obj_id, obj)
                    obj.reindexObject()
        self.rebuild_and_clean()

    def update_attribute_assignment(self):
        """
        Fixed Prospect to Lead and Billing-Contact RelationValue
        """
        items = api.content.find(portal_type='Account')
        intids = getUtility(IIntIds)
        logger.info('UPDATING ATTRIBUTES...')
        for item in items:
            obj = item.getObject()

            # Update account type
            if hasattr(obj, 'type'):
                if obj.type == 'prospect':
                    obj.type = 'lead'

            # Update RelationValue
            if hasattr(obj, 'invoice'):
                invoice_name = obj.invoice
                if invoice_name:
                    results = api.content.find(portal_type='Contact', Title=invoice_name)  # noqa
                    if results:
                        result = results[0].getObject()
                        obj.billing_contact = RelationValue(intids.getId(result))  # noqa
        self.rebuild_and_clean()

    def update_content_types(self):
        """
        Updates Content-Types
        """
        portal_catalog = api.portal.get_tool('portal_catalog')
        logger.info('UPDATING CONTENT-TYPES...')
        for key in content_type_mapping:
            for item in portal_catalog():
                obj = item.getObject()

                # Update Content-Types
                if obj.portal_type == key:
                    logger.info('{0} BEING UPDATED...'.format(key))  # noqa
                    obj.portal_type = content_type_mapping[key]

            contents = api.content.find(portal_type=key)

            if contents:
                for item in contents:
                    logger.info('{0} IN PORTAL BEING UPDATED...'.format(key))  # noqa
                    obj = item.getObject()
                    obj.portal_type = content_type_mapping[key]
            else:
                logger.info('{0} ALREADY {1}.'.format(key, content_type_mapping[key]))  # noqa
        self.rebuild_and_clean()
        self.update_classes()

    def update_displayed_types(self):
        """
        Updates Displayed-Types
        """
        logger.info('UPDATING DISPLAYED-TYPES...')
        displayed_types = api.portal.get_registry_record('plone.displayed_types')  # noqa
        displayed_types_updated = displayed_types

        for key in content_type_mapping:
            displayed_types_updated = tuple(content_type_mapping[key] if x == key else x for x in displayed_types_updated)  # noqa
            api.portal.set_registry_record('plone.displayed_types', displayed_types_updated)  # noqa
            logger.info('\n{0}\n{1}'.format(displayed_types, displayed_types_updated))  # noqa
        self.rebuild_and_clean()

    def rebuild_and_clean(self, context=None):
        """
        Rebuilds & cleans catalog
        """
        portal_catalog = api.portal.get_tool('portal_catalog')
        portal_quickinstaller = api.portal.get_tool('portal_quickinstaller')
        logger.info('REBUILDING CATALOG...')
        portal_catalog.manage_catalogRebuild()
        portal_quickinstaller.reinstallProducts(['operun.crm'])

        if context is not None:
            context.runImportStepFromProfile(default_profile, 'controlpanel')

        self.request.response.redirect('{0}/{1}'.format(self.context.absolute_url(), 'migration'))  # noqa
