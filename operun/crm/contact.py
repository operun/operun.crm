# -*- coding: utf-8 -*-
from operun.crm import MessageFactory as _
from operun.crm.config import ACCOUNT_TYPES
from plone.app.textfield import RichText
from plone.app.vocabularies.catalog import CatalogSource
from plone.dexterity.content import Item
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from zope import schema


class IContact(model.Schema):
    """
    Contact Content Type
    """

    firstname = schema.TextLine(
        title=_(u'Firstname'),
        required=False,
    )

    lastname = schema.TextLine(
        title=_(u'Lastname'),
        required=False,
    )

    type = schema.Choice(
        title=_(u'Contact Type'),
        vocabulary=ACCOUNT_TYPES,
        required=True,
    )

    # Job Title

    account = RelationChoice(
        title=_(u'Account'),
        source=CatalogSource(portal_type='Account'),
        required=False,
    )

    # Department

    phone = schema.TextLine(
        title=_(u'Phone'),
        required=False,
    )

    mobile = schema.TextLine(
        title=_(u'Mobile'),
        required=False,
    )

    email = schema.TextLine(
        title=_(u'E-Mail'),
        required=False,
    )

    notes = RichText(
        title=_(u'Notes'),
        required=False,
    )


class Contact(Item):
    """
    Contact class
    """
