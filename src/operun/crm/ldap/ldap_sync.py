# -*- coding: utf-8 -*-
"""
LDAP Sync View & Utils.
"""

from operun.crm import MessageFactory as _
from plone import api
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import ldap
import logging


logger = logging.getLogger(__name__)


class LdapSyncView(BrowserView):

    template = ViewPageTemplateFile('templates/ldap_sync.pt')

    def __call__(self):
        if self.request.form.get('form.buttons.sync'):
            self.sync_ldap_objects(self.context)
        else:
            return self.template()

    # LDAP Object Methods

    def sync_ldap_objects(self, container):
        """
        Syncs missing objects to LDAP.
        """
        connection = self.connect()
        content_type = container.Type()
        if connection:
            # Folder
            if content_type in self.types_to_sync('containers'):
                folder_contents = container.listFolderContents()
                for item in folder_contents:
                    result = self.search_for_user(item)
                    if result:
                        self.update_node_tree(item)
                        self.update_ldap_object(item)
                    else:
                        self.add_ldap_object(item)
            # Item
            else:
                result = self.search_for_user(container)
                if result:
                    self.update_node_tree(container)
                    self.update_ldap_object(container)
                else:
                    self.add_ldap_object(container)
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
            mod_attrs = self.generate_create_mod_attrs(item)
            ldap_dn = self.generate_ldap_dn(item)
            try:
                connection.add_s(ldap_dn, mod_attrs)
            except ldap.LDAPError:
                logger.info(_('An error occurred...'))
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
            mod_attrs = self.generate_update_mod_attrs(item)
            ldap_dn = self.generate_ldap_dn(item)
            self.update_node_tree(item)
            try:
                connection.modify_s(ldap_dn, mod_attrs)
            except ldap.LDAPError:
                logger.info(_('An error occurred...'))
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
                logger.info(_('An error occurred...'))
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
            mod_attrs = [
                (self.get_mapped_field(content_type, field),
                 str(getattr(item, field)))
            ]
            try:
                connection.modify_s(ldap_dn, mod_attrs)
            except ldap.LDAPError:
                logger.info(_('An error occurred...'))
        self.unbind()

    # Connection Methods

    def connect(self):
        """
        Get config credentials and connect to LDAP server.
        Check sync switch in settings.
        """
        sync_to_ldap = api.portal.get_registry_record(
            name='operun.crm.sync_to_ldap')
        ldap_server_uri = api.portal.get_registry_record(
            name='operun.crm.ldap_server_uri')
        ldap_service_user = api.portal.get_registry_record(
            name='operun.crm.ldap_service_user')
        ldap_service_pass = api.portal.get_registry_record(
            name='operun.crm.ldap_service_pass')
        if all([sync_to_ldap,
                ldap_server_uri,
                ldap_service_user,
                ldap_service_pass]):
            try:
                logger.info(_('Contacting LDAP server...'))
                self.connection = ldap.initialize(ldap_server_uri)
                self.connection.simple_bind_s(
                    ldap_service_user, ldap_service_pass)
            except ldap.LDAPError:
                logger.info(
                    _('Could not connect to {0}'.format(ldap_server_uri))
                )
            else:
                logger.info(_('Connected to {0}'.format(ldap_server_uri)))
                return self.connection
        else:
            logger.info(_('Check LDAP configuration under settings.'))

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
        ldap_objectclass_mapping = api.portal.get_registry_record(
            name='operun.crm.ldap_objectclass_mapping')
        accounts_dn = api.portal.get_registry_record(
            name='operun.crm.accounts_dn')
        users_dn = api.portal.get_registry_record(name='operun.crm.users_dn')
        # Defaults
        content_type = obj.Type()
        object_class = self.list_to_dict(
            ldap_objectclass_mapping)[content_type]
        # Check Type
        if content_type == 'Account':
            ldap_dn = accounts_dn
        if content_type == 'Contact':
            ldap_dn = users_dn
        try:
            # Returns DN(s) if user exists in LDAP
            search_result = connection.search_s(ldap_dn, ldap.SCOPE_SUBTREE, '(&(uid={0})(objectClass={1}))'.format(obj.UID(), object_class))  # noqa
        except ldap.LDAPError:
            pass
        else:
            return search_result
        self.unbind()

    def update_node_tree(self, obj):
        """
        Removes duplicate users and fixes node tree inconsistencies.
        """
        result = self.search_for_user(obj)
        current_dn = self.generate_ldap_dn(obj)
        if len(result) > 1:
            for item in result:
                old_dn = item[0]
                if old_dn != current_dn:
                    self.delete_ldap_object(old_dn)
        else:
            old_dn = result[0][0]
            obj_cn = self.generate_ldap_dn(obj, cn=True)
            obj_superior = self.generate_ldap_dn(obj, superior=True)
            if old_dn != current_dn:
                try:
                    self.connection.rename_s(old_dn, obj_cn, obj_superior)
                except ldap.LDAPError:
                    logger.info(
                        _('An error occurred, likely due to a conflicting DN.')
                    )

    # Common Utils

    def list_to_dict(self, list_of_items):
        """
        Converts list mappings into dict.
        """
        return dict(item.split('|') for item in list_of_items)

    def types_to_sync(self, type):
        """
        Return list of Content-Types to sync.
        """
        objects = ['Account', 'Contact']
        containers = ['Accounts', 'Contact']
        if 'objects':
            return objects
        elif 'containers':
            return containers
        else:
            return (objects, containers)

    def convert_to_object(self, obj):
        """
        Converts object if object has getObject() attribute.
        """
        if hasattr(obj, 'getObject'):
            obj = obj.getObject()
        elif hasattr(obj, 'object'):
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
                mod_attrs.append(
                    (self.get_mapped_field(content_type, field),
                     str(getattr(obj, field)))
                )
        return mod_attrs

    def generate_create_mod_attrs(self, obj):
        """
        Generates a mod_attrs list with objectClass and UID.
        Used in LDAP create object mode.
        """
        ldap_objectclass_mapping = api.portal.get_registry_record(
            name='operun.crm.ldap_objectclass_mapping')
        mod_attrs = self.generate_mod_attrs(obj)
        content_type = obj.Type()
        object_uid = obj.UID()
        object_class = self.list_to_dict(
            ldap_objectclass_mapping)[content_type]
        mod_attrs.append(('objectclass', object_class))
        mod_attrs.append(('uid', object_uid))
        return mod_attrs

    def generate_update_mod_attrs(self, obj):
        """
        Generates a mod_attrs list with ldap.MOD_REPLACE attribute.
        Used in LDAP update object attributes mode.
        """
        mod_attrs = self.generate_mod_attrs(obj)
        return [(ldap.MOD_REPLACE,) + item for item in mod_attrs]

    def generate_ldap_dn(self, obj, cn=False, superior=False):
        """
        Generates a DN for use in LDAP object modifiers.
        """
        # Defaults
        accounts_dn = api.portal.get_registry_record(
            name='operun.crm.accounts_dn')
        users_dn = api.portal.get_registry_record(name='operun.crm.users_dn')
        ldap_node_mapping = {
            'contact': 'contacts',
            'employee': 'employees',
            'lead': 'leads',
            'customer': 'customers',
            'vendor': 'vendors'
        }
        # Object Variables
        obj = self.convert_to_object(obj)
        object_title = obj.Title()
        content_type = obj.Type()
        account_type = obj.type
        mapped_type = ldap_node_mapping[account_type]
        # Set DN
        if content_type == 'Contact':
            ldap_node = users_dn
        if content_type == 'Account':
            ldap_node = accounts_dn
        # Construct Full-DN
        if cn and not superior:
            ldap_dn = 'cn={0}'.format(object_title)
        elif superior and not cn:
            ldap_dn = 'ou={0},{1}'.format(mapped_type, ldap_node)
        else:
            ldap_dn = 'cn={0},ou={1},{2}'.format(
                object_title, mapped_type, ldap_node)
        return ldap_dn

    def get_field_mapping(self, content_type):
        """
        Map Plone field to LDAP attribute from config.
        Return mapped dictionary as: {'field': 'attribute'}
        """
        if content_type == 'Contact':
            mapping = api.portal.get_registry_record(
                name='operun.crm.ldap_field_mapping_contact')
        elif content_type == 'Account':
            mapping = api.portal.get_registry_record(
                name='operun.crm.ldap_field_mapping_account')
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

    def check_manual_ldap_actions_enabled(self):
        """
        Check whether or not the manual LDAP actions are enabled in the config.
        """
        return api.portal.get_registry_record(
            name='operun.crm.manual_ldap_actions')


class LdapSyncAddView(LdapSyncView):

    template = ViewPageTemplateFile('templates/ldap_add.pt')

    def __call__(self):
        if self.request.form.get('form.buttons.sync'):
            self.add_ldap_object(self.context)
        else:
            return self.template()


class LdapSyncUpdateView(LdapSyncView):

    template = ViewPageTemplateFile('templates/ldap_update.pt')

    def __call__(self):
        if self.request.form.get('form.buttons.sync'):
            self.update_ldap_object(self.context)
        else:
            return self.template()


class LdapSyncDeleteView(LdapSyncView):

    template = ViewPageTemplateFile('templates/ldap_delete.pt')

    def __call__(self):
        if self.request.form.get('form.buttons.sync'):
            self.delete_ldap_object(self.context)
        else:
            return self.template()
