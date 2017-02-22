from zope import schema
from z3c.relationfield.schema import RelationChoice
from plone.dexterity.content import Item
from plone.app.textfield import RichText
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.supermodel import model
from operun.crm.account import IAccount
from operun.crm.config import ACCOUNT_TYPES
from operun.crm import MessageFactory as _


class IContact(model.Schema):
    """ Contact Content Type
    """

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

    # Job Title

    account = RelationChoice(
        title=_(u"Account"),
        source=ObjPathSourceBinder(object_provides=IAccount.__identifier__),
        required=False,
    )

    # Department

    phone = schema.TextLine(
        title=_(u"Phone"),
        required=False,
    )

    mobile = schema.TextLine(
        title=_(u"Mobile"),
        required=False,
    )

    email = schema.TextLine(
        title=_(u"E-Mail"),
        required=False,
    )

    notes = RichText(
        title=_(u"Notes"),
        required=False,
    )


class Contact(Item):
    """ Contact class
    """
