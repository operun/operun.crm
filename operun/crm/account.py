from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from plone.supermodel import model

#from z3c.relationfield.schema import RelationList, RelationChoice
#from plone.formwidget.contenttree import ObjPathSourceBinder

from operun.crm import MessageFactory as _


class IAccount(model.Schema):
    """ Account Content Type
    """

    # name stored in title

    # description 

    # type
    # selection from customer, vendor, prospect

    
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

    # billing address
    
    # postal address
    
    # related contacts