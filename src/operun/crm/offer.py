# -*- coding: utf-8 -*-
from operun.crm import MessageFactory as _
from plone.dexterity.content import Item
from plone.namedfile.field import NamedBlobFile
from plone.supermodel import model


class IOffer(model.Schema):
    """
    Offer Content Type
    """

    file = NamedBlobFile(
        title=_(u'Offer'),
        description=_(u'Please upload an offer'),
        required=False,
    )


class Offer(Item):
    """
    Offer class
    """
