# -*- coding: utf-8 -*-
import ldap
import logging

logger = logging.getLogger('Plone')

# LDAP config
KEYS = {
    'title': 'cn',
    'email': 'mail',
    'firstname': 'givenname',
    'type': 'objectclass',
    'password': 'userpassword',
    'lastname': 'sn',
    'uid': 'uid',
}

users = 'ou=users,dc=operun,dc=de'
groups = 'ou=groups,dc=operun,dc=de'

admin = 'cn=admin,dc=operun,dc=de'
password = '12345'

server = 'ldap://10.0.0.126'

# Connect
con = ldap.initialize(server)
con.simple_bind_s(admin, password)

# LDAP lists
available_users = con.search_s(users,
                               ldap.SCOPE_SUBTREE,
                               '(objectclass=inetOrgPerson)'
                               )
available_groups = con.search_s(groups,
                                ldap.SCOPE_SUBTREE,
                                '(objectclass=posixGroup)'
                                )


def update_user(contact, event):
    """
    Update user attributes in LDAP.
    """
    mod_attrs = [
        (ldap.MOD_REPLACE, KEYS['firstname'], str(contact.firstname)),
        (ldap.MOD_REPLACE, KEYS['lastname'], str(contact.lastname)),
    ]

    try:
        con.modify_s('cn={0},{1}'.format(str(contact.title), users), mod_attrs)
    except ldap.LDAPError:
        logger.info(
            '{0} could not be updated, either because the attributes do not exist or the user object has changed.'.format(str(contact.firstname))  # noqa
        )


def add_user(contact, event):
    """
    Add user in LDAP.
    """
    uid = str(contact.firstname)[0] + str(contact.lastname)

    add_record = [
        (KEYS['title'], str(contact.title)),
        (KEYS['email'], str(contact.email)),
        (KEYS['firstname'], str(contact.firstname)),
        (KEYS['type'], 'inetorgperson'),
        (KEYS['password'], password),
        (KEYS['lastname'], str(contact.lastname)),
        (KEYS['uid'], uid.lower()),
    ]

    try:
        con.add_s('cn={0},{1}'.format(str(contact.title), users), add_record)
    except ldap.LDAPError:
        logger.info(
            '{0} already exists in the LDAP directory.'.format(str(contact.title))  # noqa
        )


def delete_user(contact, event):
    """
    Delete user from LDAP.
    """
    con.delete('cn={0},{1}'.format(str(contact.title), users))
    logger.info(
        '{0} removed from LDAP directory.'.format(str(contact.title))
    )
