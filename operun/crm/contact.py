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


class IContact(model.Schema):
    """ Contact Content Type
    """

    # full name stored in title

    # description maybe faded out 

    # type
    # selection from customer, vendor, prospect

    # job title works like keywords
    
    # related account e.g. some company inc.
    
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
    