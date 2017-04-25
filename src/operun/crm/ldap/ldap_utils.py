# -*- coding: utf-8 -*-
"""
LDAP object utilities.
"""

from operun.crm.ldap.common_utils import connect
from operun.crm.ldap.common_utils import convert_to_object
from operun.crm.ldap.common_utils import generate_ldap_dn
from operun.crm.ldap.common_utils import generate_mod_attrs
from operun.crm.ldap.common_utils import get_mapped_field
from operun.crm.ldap.common_utils import unbind

import ldap
import logging


logger = logging.getLogger('Plone')


def add_ldap_object(self, item=None):
    """
    Create object in LDAP with content_type and UID.
    Get list of fields config using get_field_mapping method.
    Iterate over list and update each attribute.
    """
    connection = connect(self)
    if connection:
        if not item:
            item = self.context
        mod_attrs = generate_mod_attrs(item)
        ldap_dn = generate_ldap_dn(item)
        try:
            connection.add_s(ldap_dn, mod_attrs)
        except ldap.LDAPError:
            logger.info('An error occurred...')
    unbind(self)


def update_ldap_object(self, item=None):
    """
    Get list of attributes from get_fields_to_update method.
    Update target with constructed list of attributes and values.
    """
    connection = connect(self)
    if connection:
        if not item:
            item = self.context
        mod_attrs = generate_mod_attrs(item)
        ldap_dn = generate_ldap_dn(item)
        try:
            connection.modify_s(ldap_dn, mod_attrs)
        except ldap.LDAPError:
            logger.info('An error occurred...')
    unbind(self)


def delete_ldap_object(self, item=None):
    """
    If object in LDAP, delete object.
    """
    connection = connect(self)
    if connection:
        if not item:
            item = self.context
        ldap_dn = generate_ldap_dn(item)
        try:
            connection.delete(ldap_dn)
        except ldap.LDAPError:
            logger.info('An error occurred...')
    unbind(self)


def ldap_update_attribute(self, item=None, field=None):
    """
    Check if connection.
    If connection, update LDAP attribute.
    """
    connection = connect(self)
    if connection:
        if not item:
            item = self.context
        ldap_dn = generate_ldap_dn(item)
        item = convert_to_object(item)
        content_type = item.Type()
        mod_attrs = [(get_mapped_field(content_type, field),
                      str(getattr(item, field)))]
        try:
            connection.modify_s(ldap_dn, mod_attrs)
        except ldap.LDAPError:
            logger.info('An error occurred...')
    unbind(self)
