from plone.directives import form
from plone.dexterity.content import Container
from plone.namedfile.field import NamedBlobImage
from plone.app.textfield import RichText
from plone.supermodel import model
from zope import schema
from operun.crm import MessageFactory as _
from operun.crm.config import ACCOUNT_TYPES


class IAccount(model.Schema):
    """ Account Content Type
    """

    form.fieldset('address',
                  label=_(u"Address"),
                  fields=['address', 'invoice', 'zip', 'city', ]
                  )

    form.fieldset('notes',
                  label=_(u"Notes"),
                  fields=['text', ]
                  )

    type = schema.Choice(
        title=_(u"Account Type"),
        vocabulary=ACCOUNT_TYPES,
        required=True,
    )

    logo = NamedBlobImage(
        title=_(u"Company Logo"),
        description=_(u"Please upload an image"),
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

    address = schema.TextLine(
        title=_(u"Address"),
        required=False,
    )

    invoice = schema.TextLine(
        title=_(u"Invoice Contact"),
        required=False,
    )

    zip = schema.TextLine(
        title=_(u"ZIP"),
        required=False,
    )

    city = schema.TextLine(
        title=_(u"City"),
        required=False,
    )

    # Related Contacts

    text = RichText(
        title=_(u"Notes"),
        required=False,
    )


class Account(Container):
    """ Account class
    """
