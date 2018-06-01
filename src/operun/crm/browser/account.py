# -*- coding: utf-8 -*-
from plone import api
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

    def get_invoices(self):
        """
        Return invoices.
        """
        return api.content.find(
            context=self.context,
            portal_type='Invoice',
            sort_order='reverse',
            sort_on='title',
        )[:3]

    def get_offers(self):
        """
        Return offers.
        """
        return api.content.find(
            context=self.context,
            portal_type='Offer',
            sort_order='reverse',
            sort_on='title',
        )[:3]
