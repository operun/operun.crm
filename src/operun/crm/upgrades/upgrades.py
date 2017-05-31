# -*- coding: utf-8 -*-
"""Migration steps for operun CRM."""
from plone import api
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

import logging


default_profile = 'profile-operun.crm:default'
logger = logging.getLogger('Plone')


class MigrationsView(BrowserView):

    template = ViewPageTemplateFile('templates/upgrades.pt')

    def __call__(self):
        if self.request.form.get('form.buttons.update-types'):
            self.upgrades(content_types=True)
        if self.request.form.get('form.buttons.update-displayed'):
            self.upgrades(displayed=True)
        if self.request.form.get('form.buttons.rebuild'):
            self.upgrades()
        else:
            return self.template()

    def upgrades(self, context=None, content_types=False, displayed=False):
        """
        Update operun CRM content.
        """
        portal_catalog = api.portal.get_tool('portal_catalog')
        portal_quickinstaller = api.portal.get_tool('portal_quickinstaller')
        displayed_types = api.portal.get_registry_record('plone.displayed_types')  # noqa
        displayed_types_updated = displayed_types
        intids = getUtility(IIntIds)
        type_upgrade = {
            'operun.crm.account': 'Account',
            'operun.crm.accounts': 'Accounts',
            'operun.crm.contact': 'Contact',
            'operun.crm.contacts': 'Contacts',
            'operun.crm.invoice': 'Invoice',
            'operun.crm.offer': 'Offer',
            'operun.crm.todo': 'Todo',
            'operun.crm.todos': 'Todos',
        }
        for key in type_upgrade.keys():
            # Find & replace old Content-Types in displayed_types
            if displayed:
                displayed_types_updated = tuple(type_upgrade[key] if x == key else x for x in displayed_types_updated)  # noqa
                api.portal.set_registry_record('plone.displayed_types', displayed_types_updated)  # noqa
                logger.info('\n{0}\n{1}'.format(displayed_types, displayed_types_updated))  # noqa
            if content_types:
                for item in portal_catalog():
                    obj = item.getObject()
                    # Update Content-Types
                    if obj.portal_type == key:
                        logger.info('{0} in catalog is being updated...'.format(key))  # noqa
                        obj.portal_type = type_upgrade[key]
                    if hasattr(obj, 'type'):
                        if obj.type == 'prospect':
                            obj.type = 'lead'
                    # Update field billing_contact relation
                    if hasattr(obj, 'invoice'):
                        invoice_name = obj.invoice
                        results = api.content.find(portal_type='Account', Title=invoice_name)  # noqa
                        if results:
                            result = results[0]
                            obj.billing_contact = RelationValue(intids.getId(result))  # noqa
                contents = api.content.find(portal_type=key)
                if contents and content_types:
                    for item in contents:
                        logger.info('{0} in portal is being updated...'.format(key))  # noqa
                        obj = item.getObject()
                        obj.portal_type = type_upgrade[key]
                else:
                    logger.info('{0} already updated to {1}.'.format(key, type_upgrade[key]))  # noqa
        portal_catalog.manage_catalogRebuild()
        portal_quickinstaller.reinstallProducts(['operun.crm'])
        context.runImportStepFromProfile(default_profile, 'controlpanel')
