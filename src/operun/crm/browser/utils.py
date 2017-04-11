# -*- coding: utf-8 -*-
"""
Utils for managing LDAP directory.
"""


def assign_attribute(attribute_list=[]):
    """
    Assign field to LDAP attribute.
    """
    # NOTE: Need to store in some field...
    attribute_map = dict
    for plone_field, ldap_attribute in attribute_list:
        attribute_map[plone_field] = ldap_attribute
    return attribute_map


def user_uid_generator(givenname=None, sn=None, number=17001):
    """
    Return user UID.
    """
    first_letter = str(givenname[0])
    three_letters_surname = str(sn[:3])
    username = '{}{}{:03d}'.format(first_letter.lower(), three_letters_surname.lower(), number)  # noqa
    return username


def user_map(cn=None, mail=None, givenname=None, objectclass=None, sn=None, uid=None):  # noqa
    """
    Return user mapping for inetOrgPerson.
    """
    attribute_list = [
        ('cn', str(cn) if cn else None),
        ('mail', str(mail) if mail else None),
        ('givenname', str(givenname) if givenname else None),
        ('objectclass', str(objectclass) if objectclass else None),
        ('sn', str(sn) if sn else None),
        ('uid', str(uid) if uid else None),
    ]
    return attribute_list
