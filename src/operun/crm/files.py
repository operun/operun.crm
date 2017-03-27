# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model


class IFiles(model.Schema):
    """
    Files Content Type
    """


class Files(Container):
    """
    Files class
    """
