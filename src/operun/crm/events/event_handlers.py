# -*- coding: utf-8 -*-
"""
Event handlers for Content-Type to LDAP functions.
"""
from plone import api


def add_obj(self, event):
    """
    Object added event handler, fires add_ldap_object function.
    """
    request = event.object.REQUEST
    ldap_sync = api.content.get_view('ldap-sync', self, request)
    ldap_sync.add_ldap_object(item=self)


def update_obj(self, event):
    """
    Object modified event handler, fires update_ldap_object function.
    """
    request = event.object.REQUEST
    ldap_sync = api.content.get_view('ldap-sync', self, request)
    ldap_sync.update_ldap_object(item=self)


def delete_obj(self, event):
    """
    Object removed event handler, fires delete_ldap_object function.
    """
    request = event.object.REQUEST
    ldap_sync = api.content.get_view('ldap-sync', self, request)
    ldap_sync.delete_ldap_object(item=self)
