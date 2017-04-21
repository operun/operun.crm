# -*- coding: utf-8 -*-
from operun.crm import MessageFactory
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.supermodel.directives import fieldset
from plone.z3cform import layout
from zope import schema
from zope.interface import Interface


class ISettings(Interface):

    fieldset('DN Config', fields=['users_dn',
                                  'groups_dn',
                                  'customers_ou'])

    users_dn = schema.TextLine(
        title=MessageFactory(u'settings_root_users_dn_title',
                             default=u'Users DN'),
        description=MessageFactory(u'settings_users_dn_description',
                                   default=u'Include the full users DN path. e.g. ou=users,dc=EXAMPLE,dc=COM'),  # noqa
        required=False,
    )

    groups_dn = schema.TextLine(
        title=MessageFactory(u'settings_root_groups_dn_title',
                             default=u'Groups DN'),
        description=MessageFactory(u'settings_groups_dn_description',
                                   default=u'Include the full groups DN path. e.g. ou=groups,dc=EXAMPLE,dc=COM'),  # noqa
        required=False,
    )

    customers_ou = schema.TextLine(
        title=MessageFactory(u'settings_customers_ou_title',
                             default=u'Customers OU'),
        description=MessageFactory(u'settings_customers_ou_description',
                                   default=u'Include the customers OU, usually an extension of the users DN. e.g. ou=customers'),  # noqa
        required=False,
    )

    fieldset('Server Config', fields=['server',
                                      'admin_user',
                                      'admin_user_pw'])

    server = schema.TextLine(
        title=MessageFactory(u'settings_server_title',
                             default=u'Server'),
        default=u'localhost',
        required=False,
    )

    admin_user = schema.TextLine(
        title=MessageFactory(u'settings_admin_user_title',
                             default=u'Username'),
        required=False,
    )

    admin_user_pw = schema.Password(
        title=MessageFactory(u'settings_admin_user_pw_title',
                             default=u'Password'),
        required=False,
    )

    fieldset('Misc', fields=['online_sync',
                             'attribute_map'])

    online_sync = schema.Bool(
        title=MessageFactory(u'settings_online_sync_title',
                             default=u'Enable Online-Sync'),
        description=MessageFactory(u'settings_online_sync_description',
                                   default=u'If enabled, the CRM will attempt to sync on all modify events.'),  # noqa
        required=False,
        default=True,
    )

    attribute_map = schema.Text(
        title=MessageFactory(u'settings_attribute_map_title',
                             default=u'Attribute Mapping'),
        description=MessageFactory(u'settings_attribute_map_description',
                                   default=u'Map Plone fields to their corresponding LDAP attributes. Plone|LDAP'),  # noqa
        default=u'title|cn\nemail|mail\nfirstname|givenname\nlastname|sn',
        required=False,
    )


class SettingsEditForm(RegistryEditForm):
    schema = ISettings
    schema_prefix = 'plone.controlpanel/crm'
    label = u'CRM Settings'


SettingsView = layout.wrap_form(SettingsEditForm, ControlPanelFormWrapper)
