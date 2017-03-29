# -*- coding: utf-8 -*-
from plone.dexterity.content import Item
from plone.supermodel import model


class ITodo(model.Schema):
    """
    Todo Content Type
    """


class Todo(Item):
    """
    Todo class
    """
