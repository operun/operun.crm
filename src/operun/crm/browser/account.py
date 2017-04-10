# -*- coding: utf-8 -*-
from plone import api
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class AccountView(BrowserView):

    template = ViewPageTemplateFile('templates/account.pt')

    def __call__(self):
        """
        Custom view for account Content-Type
        """

        return self.template()

    def get_image(self):
        """
        Get object image.
        """
        context = self.context
        request = self.request
        tag = None
        if context.logo:
            images_view = api.content.get_view('images', context, request)
            scale = images_view.scale('logo', width=250, height=250, direction='thumbnail')  # noqa
            tag = scale.tag()
        return tag

    def get_attachments(self):
        """
        Get folder contents.
        """
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        invoices = catalog.searchResults(
            portal_type='Invoice', sort_order='ascending')[:3]
        offers = catalog.searchResults(
            portal_type='Offer', sort_order='ascending')[:3]

        items = {
            'invoices': invoices,
            'offers': offers,
        }

        return items
