# -*- coding: utf-8 -*-
"""
Event handlers for Content-Type to LDAP functions.
"""

from operun.crm.ldap.ldap_utils import add_ldap_object
from operun.crm.ldap.ldap_utils import delete_ldap_object
from operun.crm.ldap.ldap_utils import update_ldap_object


def add_obj(self, contact=None, event=None):
    """
    Object added event handler, fires add_ldap_object function.
    """
    add_ldap_object(self, contact)


def update_obj(self, contact=None, event=None):
    """
    Object modified event handler, fires update_ldap_object function.
    """
    update_ldap_object(self, contact)


def delete_obj(self, contact=None, event=None):
    """
    Object removed event handler, fires delete_ldap_object function.
    """
    delete_ldap_object(self, contact)
