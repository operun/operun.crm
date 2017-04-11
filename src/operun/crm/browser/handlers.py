# -*- coding: utf-8 -*-
from operun.crm.browser.utils import user_map
from operun.crm.browser.utils import user_uid_generator

import ldap
import logging


logger = logging.getLogger('Plone')

# NOTE: Should be set in control-panel
root_users = 'ou=users,dc=operun,dc=de'
root_groups = 'ou=groups,dc=operun,dc=de'

branch_customers = 'ou=customers'

server = '10.0.0.126'
crm_user = 'uid=crm,ou=services,ou=users,dc=operun,dc=de'
crm_user_pw = 'operuncrm2017'

tree = dict()


def connect(user=None, password=None, server='0.0.0.0'):
    """
    Connect to LDAP server.
    """
    url = 'ldap://{0}'.format(server)
    try:
        logger.info('Contacting LDAP server...')
        con = ldap.initialize(url)
        # Bind to LDAP server with credentials
        con.simple_bind_s(user, password)
    except ldap.LDAPError:
        logger.info('Connection failed to {0}'.format(url))
    else:
        logger.info('Connected to {0}'.format(url))
        # Output LDAP users and groups
        if root_users:
            try:
                available_users = con.search_s(root_users, ldap.SCOPE_SUBTREE, '(objectclass=inetOrgPerson)')  # noqa
                tree['users'] = available_users
            except ldap.LDAPError:
                logger.info('NOTE: Users DN restricted to this account.')
        if root_groups:
            try:
                available_groups = con.search_s(root_groups, ldap.SCOPE_SUBTREE, '(objectclass=posixGroup)')  # noqa
                tree['groups'] = available_groups
            except ldap.LDAPError:
                logger.info('NOTE: Groups DN restricted to this account.')  # noqa
        return con


def update_user(contact, event, attribute_list=[], branch=branch_customers):
    """
    Update user attributes in LDAP directory.
    attribute_list == [(attr, val),
                       (attr, val),
                       (attr, val),]
    NOTE: Attribute should be LDAP variant!
    """
    con = connect(user=crm_user, password=crm_user_pw, server=server)
    mod_attrs = []
    if not attribute_list:
        attribute_list = user_map(mail=contact.email)
    if attribute_list:
        for attribute, value in attribute_list:
            if value:
                mod_attrs.append((ldap.MOD_REPLACE, attribute, value))
    try:
        con.modify_s('cn={0}{1},{2}'.format(contact.title, ',{0}'.format(branch), root_users), mod_attrs)  # noqa
    except ldap.LDAPError:
        logger.info('{0} could not be updated.'.format(contact.title))
    con.unbind()


def add_user(contact, event, attribute_list=[], branch=branch_customers):
    """
    Add user into LDAP directory.
    attribute_list == [(attr, val),
                       (attr, val),
                       (attr, val),]
    NOTE: Attribute should be LDAP variant!
    """
    con = connect(user=crm_user,
                  password=crm_user_pw,
                  server=server)
    if not attribute_list:
        attribute_list = user_map(cn=contact.title,
                                  mail=contact.email,
                                  givenname=contact.firstname,
                                  objectclass='inetOrgPerson',
                                  sn=contact.lastname,
                                  uid=user_uid_generator(givenname=contact.firstname,  # noqa
                                                         sn=contact.lastname))
    try:
        con.add_s('cn={0}{1},{2}'.format(contact.title, ',{0}'.format(branch), root_users), attribute_list)  # noqa
    except ldap.LDAPError:
        logger.info('{0} could not be added.'.format(contact.title))
    con.unbind()


def delete_user(contact, event, branch=branch_customers):
    """
    Delete user from LDAP.
    """
    # NOTE: Should use unique ID for modification...
    con = connect(user=crm_user, password=crm_user_pw, server=server)
    title = contact.title
    con.delete('cn={0}{1},{2}'.format(title, ',{0}'.format(branch), root_users))  # noqa
    logger.info('{0} deleted from LDAP directory.'.format(title))
    con.unbind()
