"""Upgrade steps for operun.crm."""
from plone import api
import logging
from Products.CMFCore.utils import getToolByName
from plone.browserlayer.utils import unregister_layer

default_profile = 'profile-operun.crm:default'
logger = logging.getLogger("Plone")


def upgrade_ct(context):
    """Update operun.crm Content-Type names to new format."""
    logger.info("Upgrading operun.crm Content-Type names...")
    catalog = getToolByName(context, 'portal_catalog')

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
        for item in catalog():
            obj = item.getObject()
            if obj.portal_type == key:
                logger.info(
                    "{} in catalog is being updated...".format(key)
                )
                obj.portal_type = type_upgrade[key]
        if contents:
            for item in contents:
                logger.info(
                    "{} in portal is being updated...".format(key)
                )
                obj = item.getObject()
                obj.portal_type = type_upgrade[key]
        else:
            logger.info(
                "{} was not updated since no index or items were present.".format(key)  # noqa
            )

    context.runImportStepFromProfile(default_profile, 'controlpanel')


def remove_browserlayer(context):
    unregister_layer(name=u"operun.crm")

    context.runImportStepFromProfile(default_profile, 'controlpanel')
