from plone.directives import form

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from plone.formwidget.contenttree import ObjPathSourceBinder

from plone.supermodel import model

from z3c.form import group, field
from z3c.relationfield.schema import RelationChoice

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from operun.crm import MessageFactory as _
from operun.crm.invoice import IInvoice
from operun.crm.offer import IOffer
from operun.crm.config import ACCOUNT_TYPES


class IAccount(model.Schema):
    """ Account Content Type
    """

    form.fieldset('notes',
            label=_(u"Notes"),
            fields=['text',]
        )

    form.fieldset('files',
            label=_(u"Files"),
            fields=['invoices', 'offers',]
        )
    
    type = schema.Choice(
            title=_(u"Account Type"),
            vocabulary=ACCOUNT_TYPES,
            required=True,
        )
    
    logo = NamedBlobImage(
            title=_(u"Please upload an image"),
            required=False,
        )

    active = schema.Bool(
            title=_(u"Active Account"),
            required=False,
            default=True,
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

    billing_email = schema.Text(
            title=_(u"Billing E-Mail"),
            required=False,
        )
    
    postal_address = schema.Text(
            title=_(u"Postal Address"),
            required=False,
        )
    
    # related contacts

    text = RichText(
            title=_(u"Notes"),
            required=False,
        )

    offers = RelationChoice(
        title=_(u"Offers"),
        source=ObjPathSourceBinder(object_provides=IOffer.__identifier__),
        required=False,
    )

    invoices = RelationChoice(
        title=_(u"Invoices"),
        source=ObjPathSourceBinder(object_provides=IInvoice.__identifier__),
        required=False,
    )


