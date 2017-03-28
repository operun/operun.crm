# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model


class IContacts(model.Schema):
    """
    Contacts Content Type
    """


class Contacts(Container):
    """
    Contacts class
    """
