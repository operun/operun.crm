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
    portal_catalog = api.portal.get_tool(context, 'portal_catalog')
    portal_quickinstaller = api.portal.get_tool(context, 'portal_quickinstaller')  # noqa
    type_upgrade = {
        'operun.crm.account': 'Account',
        'operun.crm.accounts': 'Accounts',
        'operun.crm.contact': 'Contact',
        'operun.crm.contacts': 'Contacts',
        'operun.crm.files': 'Files',
        'operun.crm.invoice': 'Invoice',
        'operun.crm.offer': 'Offer',
        'operun.crm.todo': 'Todo',
        'operun.crm.todos': 'Todos',
    }
    for key in type_upgrade.keys():
        contents = api.content.find(portal_type=key)
        for item in portal_catalog():
            obj = item.getObject()
            if obj.portal_type == key:
                logger.info(
                    '{0} in catalog is being updated...'.format(key)
                )
                obj.portal_type = type_upgrade[key]
        if contents:
            for item in contents:
                logger.info(
                    '{0} in portal is being updated...'.format(key)
                )
                obj = item.getObject()
                obj.portal_type = type_upgrade[key]
        else:
            logger.info(
                '{0} was not updated since no index or items were present.'.format(key)  # noqa
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
