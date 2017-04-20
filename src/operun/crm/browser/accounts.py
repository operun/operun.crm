# -*- coding: utf-8 -*-
from plone import api
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class AccountsView(BrowserView):

    template = ViewPageTemplateFile('templates/accounts.pt')

    def __call__(self):
        """
        Custom accounts view
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

    def get_accounts(self):
        """
        Return contact items
        """
        return api.content.find(portal_type='Account',
                                sort_order='reverse',
                                sort_on='id')
