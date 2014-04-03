from zope import schema

from zope.schema.interfaces import IContextSourceBinder

from zope.interface import invariant, Invalid

from z3c.form import group, field
from z3c.relationfield.schema import RelationChoice

from plone.dexterity.content import Item, Container

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.supermodel import model

from operun.crm.account import IAccount
from operun.crm.config import ACCOUNT_TYPES
from operun.crm import MessageFactory as _


class IContact(model.Schema):
    """ Contact Content Type
    """

    # full name stored in title

    # description maybe faded out 

    firstname = schema.TextLine(
            title=_(u"Firstname"),
            required=False,
        )


    lastname = schema.TextLine(
            title=_(u"Lastname"),
            required=False,
        )

    type = schema.Choice(
            title=_(u"Contact Type"),
            vocabulary=ACCOUNT_TYPES,
            required=True,
        )

    # job title works like keywords

    account = RelationChoice(
        title=_(u"Account"),
        source=ObjPathSourceBinder(object_provides=IAccount.__identifier__),
        required=False,
    )
    
    # department e.g. public relations
    
    phone = schema.TextLine(
            title=_(u"Phone"),
            required=False,
        )

    mobile = schema.TextLine(
            title=_(u"Mobile"),
            required=False,
        )

    # office phone from account
    
    # office fax from account

    email = schema.TextLine(
            title=_(u"E-Mail"),
            required=False,
        )
    
    # address if other than account
    
    notes = RichText(
            title=_(u"Notes"),
            required=False,
        )


class Contact(Item):
    """ Contact class
    """
