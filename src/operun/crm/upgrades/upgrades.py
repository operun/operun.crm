# -*- coding: utf-8 -*-
"""Upgrade steps for operun.crm."""
from plone import api
from plone.browserlayer.utils import unregister_layer

import logging


default_profile = 'profile-operun.crm:default'
logger = logging.getLogger('Plone')


def upgrade_ct(context):
    """
    Update operun.crm Content-Type names to new format.
    """
    logger.info('Upgrading operun.crm Content-Types...')
    portal_catalog = api.portal.get_tool('portal_catalog')
    portal_quickinstaller = api.portal.get_tool('portal_quickinstaller')
    displayed_types = api.portal.get_registry_record('plone.displayed_types')
    displayed_types_updated = displayed_types
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
        contents = api.content.find(portal_type=key)
        # Find & replace old Content-Types in displayed_types
        displayed_types_updated = tuple(type_upgrade[key] if x == key else x for x in displayed_types_updated)  # noqa
        # Update catalog and portal entries
        for item in portal_catalog():
            obj = item.getObject()
            if obj.portal_type == key:
                logger.info(
                    '{0} in catalog is being updated...'.format(key)
                )
                obj.portal_type = type_upgrade[key]
            if hasattr(obj, 'type'):
                if obj.type == 'prospect':
                    obj.type = 'lead'
        if contents:
            for item in contents:
                logger.info(
                    '{0} in portal is being updated...'.format(key)
                )
                obj = item.getObject()
                obj.portal_type = type_upgrade[key]
        else:
            logger.info(
                '{0} already updated to {1}.'.format(key, type_upgrade[key])
            )
    api.portal.set_registry_record('plone.displayed_types', displayed_types_updated)  # noqa
    logger.info(
        'Updated displayed_types:\nOLD: {0}\nNEW: {1}'.format(displayed_types, displayed_types_updated)  # noqa
    )
    portal_catalog.manage_catalogRebuild()
    portal_quickinstaller.reinstallProducts(['operun.crm'])
    context.runImportStepFromProfile(default_profile, 'controlpanel')


def remove_browserlayer(context):
    """
    Remove browserlayer.
    """
    unregister_layer(name=u'operun.crm')
    context.runImportStepFromProfile(default_profile, 'controlpanel')
