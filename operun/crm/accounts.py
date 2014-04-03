from zope import schema
from zope.schema.interfaces import IContextSourceBinder

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.dexterity.content import Item, Container

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from plone.supermodel import model

from operun.crm import MessageFactory as _


class IAccounts(model.Schema):
    """ Accounts Content Type
    """


class Accounts(Container):
    """ Accounts class
    """