# -*- coding: utf-8 -*-
from plone import api
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class TodosView(BrowserView):

    template = ViewPageTemplateFile('templates/todos.pt')

    def __call__(self):
        """
        Custom todos view
        """

        return self.template()

    def get_todos(self):
        """
        Return todo items
        """
        items = []
        todos = api.content.find(portal_type='Todo',
                                 sort_order='reverse',
                                 sort_on='id')
        if todos:
            for todo in todos:
                items.append(todo.getObject())
        return items
