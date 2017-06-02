# -*- coding: utf-8 -*-
"""
Controlpanel configuration.
"""

from operun.crm import MessageFactory as _
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.supermodel.directives import fieldset
from plone.z3cform import layout
from zope import schema
from zope.interface import Interface


class ISettings(Interface):
    """
    Controlpanel fields.
    """

    fieldset(_(u'settings_fieldset_server',
               default=u'Server'), fields=['sync_to_ldap',
                                           'ldap_server_uri',
                                           'ldap_service_user',
                                           'ldap_service_pass'])

    sync_to_ldap = schema.Bool(
        title=_(u'settings_sync_to_ldap_title',
                default=u'LDAP Syncing'),
        description=_(u'settings_sync_to_ldap_description',
                      default=u'If enabled, the CRM will attempt an LDAP connection on sync events.'),  # noqa
        required=False,
        default=False,
    )

    ldap_server_uri = schema.TextLine(
        title=_(u'settings_ldap_server_uri_title',
                default=u'LDAP Server URI'),
        default=u'ldap://127.0.0.1',
        required=False,
    )

    ldap_service_user = schema.TextLine(
        title=_(u'settings_ldap_service_user_title',
                default=u'LDAP Service User'),
        required=False,
        default=u'cn=admin,dc=example,dc=com',
    )

    ldap_service_pass = schema.Password(
        title=_(u'settings_ldap_service_pass_title',
                default=u'LDAP Service Password'),
        required=False,
    )

    fieldset(_(u'settings_fieldset_dn',
               default=u'DN'), fields=['users_dn',
                                       'groups_dn',
                                       'accounts_dn',
                                       'archives_dn'])

    users_dn = schema.TextLine(
        title=_(u'settings_users_dn_title',
                default=u'Users DN'),
        description=_(u'settings_users_dn_description',
                      default=u'Include the users DN. e.g. ou=users,dc=example,dc=com'),  # noqa
        required=False,
        default=u'ou=users,dc=example,dc=com',
    )

    groups_dn = schema.TextLine(
        title=_(u'settings_groups_dn_title',
                default=u'Groups DN'),
        description=_(u'settings_groups_dn_description',
                      default=u'Include the groups DN. e.g. ou=groups,dc=example,dc=com'),  # noqa
        required=False,
        default=u'ou=groups,dc=example,dc=com',
    )

    accounts_dn = schema.TextLine(
        title=_(u'settings_accounts_dn_title',
                default=u'Accounts DN'),
        description=_(u'settings_accounts_dn_description',
                      default=u'Include the accounts DN. e.g. ou=accounts,dc=example,dc=com'),  # noqa
        required=False,
        default=u'ou=accounts,dc=example,dc=com',
    )

    archives_dn = schema.TextLine(
        title=_(u'settings_archives_dn_title',
                default=u'Archives DN'),
        description=_(u'settings_archives_dn_description',
                      default=u'Include the archives DN. e.g. ou=archives,dc=example,dc=com'),  # noqa
        required=False,
        default=u'ou=archives,dc=example,dc=com',
    )

    fieldset(_(u'settings_fieldset_mapping',
               default=u'Mapping'), fields=['ldap_field_mapping_contact',
                                            'ldap_field_mapping_account',
                                            'ldap_objectclass_mapping'])

    ldap_field_mapping_contact = schema.List(
        title=_(u'settings_ldap_field_mapping_contact_title',
                default=u'Contact Attribute Mapping'),
        description=_(u'settings_ldap_field_mapping_contact_description',
                      default=u'Map Plone fields to their corresponding LDAP attributes. Plone|LDAP'),  # noqa
        value_type=schema.TextLine(),
        default=['title|cn',
                 'email|mail',
                 'firstname|givenname',
                 'lastname|sn'],
        required=False,
    )

    ldap_field_mapping_account = schema.List(
        title=_(u'settings_ldap_field_mapping_account_title',
                default=u'Account Attribute Mapping'),
        description=_(u'settings_ldap_field_mapping_account_description',
                      default=u'Map Plone fields to their corresponding LDAP attributes. Plone|LDAP'),  # noqa
        value_type=schema.TextLine(),
        default=['title|cn',
                 'billing_email|mail',
                 'ceo|givenname',
                 'type|sn'],
        required=False,
    )

    ldap_objectclass_mapping = schema.List(
        title=_(u'settings_ldap_objectclass_mapping_title',
                default=u'Content-Type to objectClass Mapping'),
        description=_(u'settings_ldap_objectclass_mapping_description',
                      default=u'Map Plone Content-Type to an LDAP objectClass. Plone|LDAP'),  # noqa
        value_type=schema.TextLine(),
        default=['Group|posixGroup',
                 'Account|inetOrgPerson',
                 'Contact|inetOrgPerson'],
        required=False,
    )

    fieldset(_(u'settings_fieldset_other',
               default=u'Other'), fields=['manual_ldap_actions',
                                          'ldap_archiving'])

    manual_ldap_actions = schema.Bool(
        title=_(u'settings_manual_ldap_actions_title',
                default=u'Manual LDAP Actions'),
        description=_(u'settings_manual_ldap_actions_description',
                      default=u'Enable manual LDAP controls in the actions menu.'),  # noqa
        required=False,
        default=False,
    )

    ldap_archiving = schema.Bool(
        title=_(u'settings_ldap_archiving_title',
                default=u'LDAP Archiving'),
        description=_(u'settings_ldap_archiving_description',
                      default=u'If enabled, duplicate LDAP entries will be archived instead of deleted.'),  # noqa
        required=False,
        default=False,
    )


class SettingsEditForm(RegistryEditForm):
    schema = ISettings
    schema_prefix = 'operun.crm'
    label = _(u'crm_settings_title', default=u'CRM Settings')


SettingsView = layout.wrap_form(SettingsEditForm, ControlPanelFormWrapper)
