# -*- coding: utf-8 -*-
"""
LDAP Sync view & utilities.
"""

from operun.crm import MessageFactory as _
from plone import api
from Products.CMFPlone.utils import safe_hasattr
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter

import datetime
import ldap
import logging


logger = logging.getLogger(__name__)


class LdapSyncView(BrowserView):

    template = ViewPageTemplateFile('templates/ldap_sync.pt')

    def __call__(self):
        if self.request.form.get('form.buttons.sync'):
            context = self.context
            self.sync_ldap_container(context)
        else:
            return self.template()

    # LDAP object methods

    def sync_ldap_container(self, container):
        """
        Syncs missing objects to LDAP.
        """
        connection = self.connect()
        content_type = container.Type()
        if connection:
            self.ldap_remove_stale_objects(container)
            if content_type in self.types_to_sync('containers'):
                folder_contents = container.listFolderContents()
                for item in folder_contents:
                    result = self.search_for_user(item)
                    if result:
                        self.update_container(item)
                        self.update_ldap_object(item)
                    else:
                        self.add_ldap_object(item)
        self.unbind()

    def add_ldap_object(self, item=None):
        """
        Create object in LDAP with content_type and UID.
        Get list of fields config using get_field_mapping method.
        Iterate over list and update each attribute.
        """
        connection = self.connect()
        if connection:
            if not item:
                item = self.context
            mod_attrs = self.create_mod_attrs(item)
            ldap_dn = self.generate_ldap_dn(item)
            try:
                connection.add_s(ldap_dn, mod_attrs)
            except ldap.LDAPError:
                logger.info(_('An error occurred in add_ldap_object()'))
        self.unbind()

    def update_ldap_object(self, item=None):
        """
        Get list of attributes from get_fields_to_update method.
        Update target with constructed list of attributes and values.
        """
        connection = self.connect()
        if connection:
            if not item:
                item = self.context
            mod_attrs = self.update_mod_attrs(item)
            ldap_dn = self.generate_ldap_dn(item)
            self.update_container(item)
            try:
                connection.modify_s(ldap_dn, mod_attrs)
            except ldap.LDAPError:
                logger.info(_('An error occurred in update_ldap_object()'))
        self.unbind()

    def delete_ldap_object(self, item=None):
        """
        If object in LDAP, delete object.
        """
        connection = self.connect()
        if connection:
            if not item:
                item = self.context
                ldap_dn = self.generate_ldap_dn(item)
            else:
                ldap_dn = item
                if not isinstance(item, str):
                    ldap_dn = self.generate_ldap_dn(item)
            try:
                connection.delete(ldap_dn)
            except ldap.LDAPError:
                logger.info(_('An error occurred in delete_ldap_object()'))
        self.unbind()

    def ldap_update_attribute(self, item=None, field=None):
        """
        Check if connection.
        If connection, update LDAP attribute.
        """
        connection = self.connect()
        if connection:
            if not item:
                item = self.context
            ldap_dn = self.generate_ldap_dn(item)
            item = self.convert_to_object(item)
            content_type = item.Type()
            mod_attrs = [(self.get_mapped_field(content_type, field), str(getattr(item, field)))]  # noqa
            try:
                connection.modify_s(ldap_dn, mod_attrs)
            except ldap.LDAPError:
                logger.info(_('An error occurred in ldap_update_attribute()'))
        self.unbind()

    # Connection methods

    def connect(self):
        """
        Get config credentials and connect to LDAP server.
        Check sync switch in settings.
        """
        sync_to_ldap = api.portal.get_registry_record(name='operun.crm.sync_to_ldap')  # noqa
        ldap_server_uri = api.portal.get_registry_record(name='operun.crm.ldap_server_uri')  # noqa
        ldap_service_user = api.portal.get_registry_record(name='operun.crm.ldap_service_user')  # noqa
        ldap_service_pass = api.portal.get_registry_record(name='operun.crm.ldap_service_pass')  # noqa
        if all([sync_to_ldap,
                ldap_server_uri,
                ldap_service_user,
                ldap_service_pass]):
            try:
                logger.info(_('Contacting LDAP server...'))
                self.connection = ldap.initialize(ldap_server_uri)
                self.connection.simple_bind_s(ldap_service_user, ldap_service_pass)  # noqa
            except ldap.LDAPError:
                logger.info(_('Could not connect to {0}'.format(ldap_server_uri)))  # noqa
            else:
                logger.info(_('Connected to {0}'.format(ldap_server_uri)))
                return self.connection
        else:
            logger.info(_('Check LDAP config.'))

    def unbind(self):
        """
        Unbind connection.
        """
        try:
            self.connection.unbind()
        except AttributeError:
            pass
        else:
            logger.info(_('Disconnected from LDAP server...'))

    def search_for_user(self, obj):
        """
        Search for user by UID and return DN from LDAP.
        Can be used as conditional method if user exists in LDAP.
        Should take single object, either passed or through iteration.
        """
        connection = self.connect()
        ldap_objectclass_mapping = api.portal.get_registry_record(name='operun.crm.ldap_objectclass_mapping')  # noqa
        accounts_dn = api.portal.get_registry_record(name='operun.crm.accounts_dn')  # noqa
        users_dn = api.portal.get_registry_record(name='operun.crm.users_dn')
        # Defaults
        content_type = obj.Type()
        object_class = self.list_to_dict(ldap_objectclass_mapping)[content_type]  # noqa
        # Check Content-Type
        if content_type == 'Account':
            ldap_dn = accounts_dn
        if content_type == 'Contact':
            ldap_dn = users_dn
        try:
            # Return DN(s) if user exists in LDAP
            search_result = connection.search_s(ldap_dn, ldap.SCOPE_SUBTREE, '(&(uid={0})(objectClass={1}))'.format(obj.UID(), object_class))  # noqa
        except ldap.LDAPError:
            pass
        else:
            return search_result
        self.unbind()

    def update_container(self, obj):
        """
        Removes duplicate users and updates containers.
        """
        # Defaults
        ldap_archiving = api.portal.get_registry_record(name='operun.crm.ldap_archiving')  # noqa
        result = self.search_for_user(obj)
        current_dn = self.generate_ldap_dn(obj)
        # Length should be 1 since we query by UID
        if len(result) > 1:
            for item in result:
                old_dn = item[0]
                if old_dn != current_dn:
                    if ldap_archiving:
                        self.archive_item(item)
                    else:
                        self.delete_ldap_object(old_dn)
        # If single result, check DN and update it
        elif len(result) == 1:
            old_dn = result[0][0]
            obj_cn = self.generate_ldap_cn(obj)
            obj_superior = self.generate_ldap_superior(obj)
            if old_dn != current_dn:
                try:
                    self.connection.rename_s(old_dn, obj_cn, obj_superior)
                except ldap.LDAPError:
                    logger.info(_('An error occurred, likely due to a conflicting DN.'))  # noqa
        else:
            logger.info(_('An error occurred in update_node_tree()'))

    def archive_item(self, item):
        """
        If enabled, method will attempt to archive duplicate entry.
        """
        archives_dn = api.portal.get_registry_record(name='operun.crm.archives_dn')  # noqa
        old_dn = item[0]
        item_cn = item[1]['cn'][0]
        try:
            self.connection.rename_s(old_dn, 'cn={0} {1}'.format(item_cn, str(datetime.datetime.now())), archives_dn)  # noqa
        except ldap.LDAPError:
            logger.info(_('An error occurred, item couldn\'t be archived.'))  # noqa

    def ldap_remove_stale_objects(self, container):
        """
        Remove objects by UID from LDAP that no-longer exist in Plone.
        """
        connection = self.connect()
        # Defaults
        ldap_objectclass_mapping = api.portal.get_registry_record(name='operun.crm.ldap_objectclass_mapping')  # noqa
        accounts_dn = api.portal.get_registry_record(name='operun.crm.accounts_dn')  # noqa
        users_dn = api.portal.get_registry_record(name='operun.crm.users_dn')
        content_type = container.Type()
        # Set Content-Type based variables
        if content_type == 'Accounts':
            portal_type = 'Account'
            ldap_dn = accounts_dn
        if content_type == 'Contacts':
            portal_type = 'Contact'
            ldap_dn = users_dn
        # Construct search query
        object_class = self.list_to_dict(ldap_objectclass_mapping)[portal_type]
        ldap_results = connection.search_s(ldap_dn, ldap.SCOPE_SUBTREE, '(objectClass={0})'.format(object_class))  # noqa
        # Loop through search results
        for item in ldap_results:
            item_dn = item[0]
            item_uid = item[1]['uid'][0]
            # If no object with UID in Plone, delete from LDAP
            if not api.content.find(portal_type=portal_type, UID=item_uid):
                self.delete_ldap_object(item_dn)
                logger.info(_('Deleted LDAP entry for {0}'.format(item_dn)))  # noqa

    # Common utils

    def list_to_dict(self, list_of_items):
        """
        Converts list mappings into dict.
        """
        return dict(item.split('|') for item in list_of_items)

    def types_to_sync(self, portal_type):
        """
        Return list of Content-Types to sync.
        """
        objects = ['Account', 'Contact']
        containers = ['Accounts', 'Contacts']
        if portal_type == 'objects':
            return objects
        if portal_type == 'containers':
            return containers
        return (objects, containers)

    def convert_to_object(self, obj):
        """
        Converts object if object has getObject() attribute.
        """
        if safe_hasattr(obj, 'getObject'):
            obj = obj.getObject()
        elif safe_hasattr(obj, 'object'):
            obj = obj.object
        return obj

    def generate_mod_attrs(self, obj):
        """
        Generate list of attributes and values for use in LDAP.
        """
        mod_attrs = []
        obj = self.convert_to_object(obj)
        content_type = obj.Type()
        if content_type in self.types_to_sync('objects'):
            for field in self.get_fields_to_update(content_type):
                # Create modifiable attribute from fields to update
                mod_attrs.append((self.get_mapped_field(content_type, field), str(getattr(obj, field))))  # noqa
        return mod_attrs

    def create_mod_attrs(self, obj):
        """
        Generates a mod_attrs list with objectClass and UID.
        Used in LDAP create object mode.
        """
        # Defaults
        ldap_objectclass_mapping = api.portal.get_registry_record(name='operun.crm.ldap_objectclass_mapping')  # noqa
        mod_attrs = self.generate_mod_attrs(obj)
        # Set variables
        content_type = obj.Type()
        object_uid = obj.UID()
        object_class = self.list_to_dict(ldap_objectclass_mapping)[content_type]  # noqa
        # Append objectClass and UID to attribute tuple
        mod_attrs.append(('objectclass', [str(object_class)]))
        mod_attrs.append(('uid', object_uid))
        return mod_attrs

    def update_mod_attrs(self, obj):
        """
        Generates a mod_attrs list with ldap.MOD_REPLACE attribute.
        Used in LDAP update object attributes mode.
        """
        mod_attrs = self.generate_mod_attrs(obj)
        return [(ldap.MOD_REPLACE,) + item for item in mod_attrs]

    def generate_ldap_dn(self, obj):
        """
        Return full DN.
        """
        cn = self.generate_ldap_cn(obj)
        superior = self.generate_ldap_superior(obj)
        return '{0},{1}'.format(cn, superior)

    def generate_ldap_cn(self, obj):
        """
        Return CN only.
        """
        return 'cn={0}'.format(obj.Title())

    def generate_ldap_superior(self, obj):
        """
        Return superior only.
        """
        # Defaults
        accounts_dn = api.portal.get_registry_record(name='operun.crm.accounts_dn')  # noqa
        users_dn = api.portal.get_registry_record(name='operun.crm.users_dn')
        ldap_node_mapping = {
            'contact': 'contacts',
            'employee': 'employees',
            'lead': 'leads',
            'customer': 'customers',
            'vendor': 'vendors'
        }
        # Object variables
        obj = self.convert_to_object(obj)
        content_type = obj.Type()
        account_type = obj.type
        mapped_type = 'ou={0},'.format(ldap_node_mapping[account_type])
        # Set DN
        if content_type == 'Contact':
            ldap_node = users_dn
        if content_type == 'Account':
            ldap_node = accounts_dn
            mapped_type = ''
        return '{0}{1}'.format(mapped_type, ldap_node)

    def get_field_mapping(self, content_type):
        """
        Map Plone field to LDAP attribute from config.
        Return mapped dictionary as: {'field': 'attribute'}
        """
        if content_type == 'Contact':
            mapping = api.portal.get_registry_record(name='operun.crm.ldap_field_mapping_contact')  # noqa
        elif content_type == 'Account':
            mapping = api.portal.get_registry_record(name='operun.crm.ldap_field_mapping_account')  # noqa
        if mapping:
            return self.list_to_dict(mapping)

    def get_mapped_field(self, content_type, field):
        """
        Return mapped field value.
        """
        field_mapping = self.get_field_mapping(content_type)
        return field_mapping[field]

    def get_fields_to_update(self, content_type):
        """
        Return list of assigned Plone fields from get_field_mapping method.
        """
        return self.get_field_mapping(content_type).keys()

    # Action switches

    def ldap_actions_enabled(self):
        """
        Check whether or not the manual LDAP actions are enabled in the config.
        """
        sync_to_ldap = api.portal.get_registry_record(name='operun.crm.sync_to_ldap')  # noqa
        if sync_to_ldap:
            return api.portal.get_registry_record(name='operun.crm.manual_ldap_actions')  # noqa

    def access_to_sync_action(self):
        """
        Check if sync action allowed in current interface.
        """
        if self.ldap_actions_enabled():
            # Import Content-Type interfaces
            from operun.crm.content.accounts import IAccounts
            from operun.crm.content.contacts import IContacts
            # Assign current context
            context_helper = getMultiAdapter((self.context, self.request), name='plone_context_state')  # noqa
            canonical = context_helper.canonical_object()
            # See if current context matches required interfaces
            accounts_provided = IAccounts.providedBy(canonical)
            contacts_provided = IContacts.providedBy(canonical)
            if accounts_provided or contacts_provided:
                return True

    def access_to_standard_actions(self):
        """
        Check if standard actions allowed in current interface.
        """
        if self.ldap_actions_enabled():
            # Import Content-Type interfaces
            from operun.crm.content.account import IAccount
            from operun.crm.content.contact import IContact
            # Assign current context
            context_helper = getMultiAdapter((self.context, self.request), name='plone_context_state')  # noqa
            canonical = context_helper.canonical_object()
            # See if current context matches required interfaces
            account_provided = IAccount.providedBy(canonical)
            contact_provided = IContact.providedBy(canonical)
            if account_provided or contact_provided:
                return True


class LdapAddView(LdapSyncView):

    template = ViewPageTemplateFile('templates/ldap_add.pt')

    def __call__(self):
        if self.request.form.get('form.buttons.sync'):
            context = self.context
            # Pass current context Contact/Account into method
            self.add_ldap_object(context)
        else:
            return self.template()


class LdapUpdateView(LdapSyncView):

    template = ViewPageTemplateFile('templates/ldap_update.pt')

    def __call__(self):
        if self.request.form.get('form.buttons.sync'):
            context = self.context
            # Pass current context Contact/Account into method
            self.update_ldap_object(context)
        else:
            return self.template()


class LdapDeleteView(LdapSyncView):

    template = ViewPageTemplateFile('templates/ldap_delete.pt')

    def __call__(self):
        if self.request.form.get('form.buttons.sync'):
            context = self.context
            # Pass current context Contact/Account into method
            self.delete_ldap_object(context)
        else:
            return self.template()
