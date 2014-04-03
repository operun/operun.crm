from plone.directives import form
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.supermodel import model

from operun.crm import MessageFactory as _


class IOffer(model.Schema):
    """ Offer Content Type
    """
    
    file = NamedBlobFile(
        title=_(u"Offer"),
        description=_(u"Please upload a offer"),
        required=False,
        )