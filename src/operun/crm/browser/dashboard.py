# -*- coding: utf-8 -*-

from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class DashboardView(BrowserView):

    template = ViewPageTemplateFile('templates/dashboard.pt')

    def __call__(self):
        return self.template()

    def return_portal_url(self):
        return api.portal.get().absolute_url()
