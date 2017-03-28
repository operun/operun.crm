# -*- coding: utf-8 -*-
from operun.crm import MessageFactory as _
from plone.dexterity.content import Item
from plone.namedfile.field import NamedBlobFile
from plone.supermodel import model


class IInvoice(model.Schema):
    """
    Invoice Content Type
    """

    file = NamedBlobFile(
        title=_(u'Invoice'),
        description=_(u'Please upload an invoice'),
        required=False,
    )


class Invoice(Item):
    """
    Invoice class
    """
