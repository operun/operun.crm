# -*- coding: utf-8 -*-
import ldap
import logging


logger = logging.getLogger('Plone')

# NOTE: Should be set in control-panel
root_users = 'ou=users,dc=operun,dc=de'
root_groups = 'ou=groups,dc=operun,dc=de'

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
                logger.info('NOTE: User does not have access to the users DN.')
        if root_groups:
            try:
                available_groups = con.search_s(root_groups, ldap.SCOPE_SUBTREE, '(objectclass=posixGroup)')  # noqa
                tree['groups'] = available_groups
            except ldap.LDAPError:
                logger.info('NOTE: User does not have access to the groups DN.')  # noqa
        return con


def assign_attribute(attribute_list=[]):
    """
    Assign field to LDAP attribute.
    """
    # NOTE: Need to store dict somewhere..?
    attribute_map = dict
    for plone_field, ldap_attribute in attribute_list:
        attribute_map[plone_field] = ldap_attribute
    return attribute_map


def update_user(contact, event, attribute_list=[], branch='ou=customers'):
    """
    Update user attributes in LDAP directory.
    attribute_list == [(attr, val),
                       (attr, val),
                       (attr, val),]
    NOTE: Attribute should be LDAP variant!
    """
    con = connect(user=crm_user, password=crm_user_pw, server=server)
    mod_attrs = []
    title = contact.title
    if attribute_list:
        for attribute, value in attribute_list:
            mod_attrs.append((ldap.MOD_REPLACE, attribute, value))
    try:
        con.modify_s('cn={0}{1},{2}'.format(title, ',{0}'.format(branch), root_users), mod_attrs)  # noqa
    except ldap.LDAPError:
        logger.info('{0} could not be updated.'.format(title))
    con.unbind()


def add_user(contact, event, attribute_list=[], branch='ou=customers'):
    """
    Add user into LDAP directory.
    attribute_list == [(attr, val),
                       (attr, val),
                       (attr, val),]
    NOTE: Attribute should be LDAP variant!
    """
    con = connect(user=crm_user, password=crm_user_pw, server=server)
    title = contact.title
    try:
        con.add_s('cn={0}{1},{2}'.format(title, ',{0}'.format(branch), root_users), attribute_list)  # noqa
    except ldap.LDAPError:
        logger.info('{0} could not be added.'.format(title))
    con.unbind()


def delete_user(contact, event, branch='ou=customers'):
    """
    Delete user from LDAP.
    """
    # NOTE: Should use UID instead of name in-case object changes...
    con = connect(user=crm_user, password=crm_user_pw, server=server)
    title = contact.title
    con.delete('cn={0}{1},{2}'.format(title, ',{0}'.format(branch), root_users))  # noqa
    logger.info('{0} deleted from LDAP directory.'.format(title))
    con.unbind()
