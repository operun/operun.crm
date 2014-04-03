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

from operun.crm import MessageFactory as _


class IContacts(model.Schema):
    """ Contacts Content Type
    """


class Contacts(Container):
    """ Contacts class
    """
