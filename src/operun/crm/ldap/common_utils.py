# -*- coding: utf-8 -*-
"""
Utils for LDAP functionality.
"""

from plone import api

import ldap
import logging


logger = logging.getLogger('Plone')


def connect(self):
    """
    Get config credentials and connect to LDAP server.
    Check sync switch in settings.
    """
    # Defaults
    sync_to_ldap = api.portal.get_registry_record(
        name='operun.crm.sync_to_ldap')
    ldap_server_uri = api.portal.get_registry_record(
        name='operun.crm.ldap_server_uri')
    ldap_service_user = api.portal.get_registry_record(
        name='operun.crm.ldap_service_user')
    ldap_service_pass = api.portal.get_registry_record(
        name='operun.crm.ldap_service_pass')
    # Logic
    if all([sync_to_ldap,
            ldap_server_uri,
            ldap_service_user,
            ldap_service_pass]):
        try:
            logger.info('Contacting LDAP server...')
            self.connection = ldap.initialize(ldap_server_uri)
            self.connection.simple_bind_s(ldap_service_user, ldap_service_pass)
        except ldap.LDAPError:
            logger.info('Could not connect to {0}'.format(ldap_server_uri))
        else:
            logger.info('Connected to {0}'.format(ldap_server_uri))
            return self.connection
    else:
        logger.info('Check LDAP configuration under settings.')


def unbind(self):
    """
    Unbind connection.
    """
    try:
        self.connection.unbind()
    except AttributeError:
        logger.info('No connection!')
    else:
        logger.info('Disconnected from LDAP server...')


def list_to_dict(list_of_items):
    """
    Converts list mappings into dict.
    """
    return dict(item.split('|') for item in list_of_items)


def types_to_sync():
    """
    Return list of Content-Types to sync.
    """
    types = ['Account', 'Contact']
    return types


def convert_to_object(obj):
    """
    Converts object if object has getObject() attribute.
    """
    if hasattr(obj, 'getObject'):
        obj = obj.getObject()
    elif hasattr(obj, 'object'):
        obj = obj.object
    return obj


def generate_mod_attrs(obj):
    """
    Generate list of attributes and values for use in LDAP.
    """
    # Defaults
    mod_attrs = []
    obj = convert_to_object(obj)
    content_type = obj.Type()
    object_uid = obj.UID()
    # Logic
    if content_type in types_to_sync():
        for field in get_fields_to_update(content_type):
            mod_attrs.append(
                (get_mapped_field(
                    content_type, field
                ), str(getattr(obj, field)))
            )

    # NOTE: Appends the default objectClass to mod_attrs, this should
    # be moved to the settings and handled as a selectable value..?
    class_list = {
        'Account': 'posixGroup',
        'Contact': 'inetOrgPerson',
    }
    mod_attrs.append(('objectclass', class_list[content_type]))

    # NOTE: Appends the UID to mod_attrs for identification, maybe move
    # this to a settings switch if the user wishes to use the Plone UID..?
    mod_attrs.append(('uid', object_uid))

    return mod_attrs


def generate_ldap_dn(obj, query=False):
    """
    Generate path for LDAP modification.
    """
    users_dn = api.portal.get_registry_record(name='operun.crm.users_dn')
    accounts_dn = api.portal.get_registry_record(name='operun.crm.accounts_dn')
    obj = convert_to_object(obj)
    content_type = obj.Type()

    # NOTE: Explicit DN construction, should be refactored...
    if obj and users_dn or accounts_dn:
        if content_type == 'Contact':
            object_title = obj.Title()
            object_type = obj.type
            ldap_node = 'cn={0},ou={1}s'.format(object_title, object_type)
            return '{0},{1}'.format(ldap_node, users_dn)
        elif content_type == 'Account':
            object_title = obj.Title()
            ldap_node = 'cn={0}'.format(object_title)
            return '{0},{1}'.format(ldap_node, accounts_dn)


def get_field_mapping(content_type):
    """
    Map Plone field to LDAP attribute from config.
    Return mapped dictionary as: {'field': 'attribute'}
    """
    # Defaults
    contact_mapping = api.portal.get_registry_record(
        name='operun.crm.ldap_field_mapping_contact')
    account_mapping = api.portal.get_registry_record(
        name='operun.crm.ldap_field_mapping_account')
    # Logic
    if content_type:
        if content_type == 'Contact':
            return list_to_dict(contact_mapping)
        elif content_type == 'Account':
            return list_to_dict(account_mapping)
    else:
        return None


def get_mapped_field(content_type, field):
    """
    Return mapped field value.
    """
    field_mapping = get_field_mapping(content_type)
    return field_mapping[field]


def get_fields_to_update(content_type):
    """
    Return list of assigned Plone fields from get_field_mapping method.
    """
    return get_field_mapping(content_type).keys()
