# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class AccountView(BrowserView):

    template = ViewPageTemplateFile('templates/account.pt')

    def __call__(self):
        """
        Custom view for account Content-Type
        """

        return self.template()
