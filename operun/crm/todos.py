# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model


class ITodos(model.Schema):
    """
    Todos Content Type
    """


class Todos(Container):
    """
    Todos class
    """
