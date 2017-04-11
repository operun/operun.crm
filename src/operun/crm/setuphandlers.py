# -*- coding: utf-8 -*-
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'operun.crm:uninstall',
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    _displayed_types()
    _set_mark_special_links()


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def _displayed_types():
    """
    Add Training to displayed types.
    """
    types = api.portal.get_registry_record('plone.displayed_types')
    types = types + ('Accounts', 'Contacts', 'Todos')
    api.portal.set_registry_record('plone.displayed_types', types)


def _set_mark_special_links():
    """
    Removes external link icon.
    """
    api.portal.set_registry_record('plone.mark_special_links', False)
