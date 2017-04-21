# -*- coding: utf-8 -*-
from plone import api
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ContactsView(BrowserView):

    template = ViewPageTemplateFile('templates/contacts.pt')

    def __call__(self):
        """
        Custom contacts view
        """

        return self.template()

    def get_image(self):
        """
        Get object image.
        """
        context = self.context
        request = self.request
        tag = None
        if context.image:
            images_view = api.content.get_view('images', context, request)
            scale = images_view.scale('image')
            tag = scale.tag()
        return tag

    def get_contacts(self):
        """
        Return contact items
        """
        items = []
        contacts = api.content.find(portal_type='Contact',
                                    sort_order='reverse',
                                    sort_on='id')
        if contacts:
            for contact in contacts:
                items.append(contact.getObject())
        return items
