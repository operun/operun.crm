from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field
from z3c.relationfield.schema import RelationChoice

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from plone.formwidget.contenttree import ObjPathSourceBinder

from plone.supermodel import model

from operun.crm import MessageFactory as _
from operun.crm.config import ACCOUNT_TYPES


class IAccount(model.Schema):
    """ Account Content Type
    """

    type = schema.Choice(
            title=_(u"Account Type"),
            vocabulary=ACCOUNT_TYPES,
            required=True,
        )
    
    text = RichText(
            title=_(u"Notes"),
            required=False,
        )
    
    phone = schema.TextLine(
            title=_(u"Phone"),
            required=False,
        )

    fax = schema.TextLine(
            title=_(u"Fax"),
            required=False,
        )
    
    website = schema.TextLine(
            title=_(u"Website"),
            required=False,
        )

    billing_address = schema.Text(
            title=_(u"Billing Address"),
            required=False,
        )
    
    postal_address = schema.Text(
            title=_(u"Postal Address"),
            required=False,
        )
    
    # related contacts
