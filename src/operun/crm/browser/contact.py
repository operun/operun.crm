# -*- coding: utf-8 -*-
from plone import api
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ContactView(BrowserView):

    template = ViewPageTemplateFile('templates/contact.pt')

    def __call__(self):
        """
        Custom view for contact Content-Type
        """

        return self.template()

    def get_image(self):
        """
        Get object image.
        """
        context = self.context
        request = self.request
        tag = None
        if context.businesscard:
            images_view = api.content.get_view('images', context, request)
            scale = images_view.scale('businesscard', width=250, height=250, direction='thumbnail')  # noqa
            tag = scale.tag()
        return tag
