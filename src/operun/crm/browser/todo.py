# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class TodoView(BrowserView):

    template = ViewPageTemplateFile('templates/todo.pt')

    def __call__(self):
        """
        Custom view for todo Content-Type
        """

        return self.template()
