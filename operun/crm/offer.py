from plone.namedfile.field import NamedBlobFile
from plone.supermodel import model

from plone.dexterity.content import Item

from operun.crm import MessageFactory as _


class IOffer(model.Schema):
    """
    Offer Content Type
    """

    file = NamedBlobFile(
        title=_(u"Offer"),
        description=_(u"Please upload an offer"),
        required=False,
    )


class Offer(Item):
    """
    Offer class
    """
