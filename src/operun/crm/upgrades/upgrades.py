# -*- coding: utf-8 -*-
"""
Migration steps for operun CRM.
"""
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.interface import alsoProvides
from zope.intid.interfaces import IIntIds

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


class MigrationsView(BrowserView):

    template = ViewPageTemplateFile('templates/upgrades.pt')

    def __call__(self):
        if self.request.form.get('form.buttons.update-attribute-assignment'):
            self.update_attribute_assignment()
        if self.request.form.get('form.buttons.update-content-types'):
            self.update_content_types()
        if self.request.form.get('form.buttons.update-displayed-types'):
            self.update_displayed_types()
        if self.request.form.get('form.buttons.rebuild-and-clean'):
            self.rebuild_and_clean()
        else:
            return self.template()

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
                    logger.info('{0} in catalog is being updated...'.format(key))  # noqa
                    obj.portal_type = content_type_mapping[key]

            contents = api.content.find(portal_type=key)

            if contents:
                for item in contents:
                    logger.info('{0} in portal is being updated...'.format(key))  # noqa
                    obj = item.getObject()
                    obj.portal_type = content_type_mapping[key]
            else:
                logger.info('{0} already updated to {1}.'.format(key, content_type_mapping[key]))  # noqa

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

    def rebuild_and_clean(self, context=None):
        """
        Rebuilds & cleans catalog
        """
        alsoProvides(self.request, IDisableCSRFProtection)
        portal_catalog = api.portal.get_tool('portal_catalog')
        portal_quickinstaller = api.portal.get_tool('portal_quickinstaller')
        logger.info('REBUILDING CATALOG...')
        portal_catalog.manage_catalogRebuild()
        portal_quickinstaller.reinstallProducts(['operun.crm'])

        if context is not None:
            context.runImportStepFromProfile(default_profile, 'controlpanel')

        self.request.response.redirect('{0}/{1}'.format(self.context.absolute_url(), 'migration'))  # noqa
