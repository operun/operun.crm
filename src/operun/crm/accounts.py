# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model


class IAccounts(model.Schema):
    """
    Accounts Content Type
    """


class Accounts(Container):
    """
    Accounts class
    """
