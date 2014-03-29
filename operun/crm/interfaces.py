from z3c.form import interfaces

from zope.interface import Interface
from zope import schema

from zope.container.constraints import contains

from operun.crm import MessageFactory as _


class IIsFrontpage(Interface):
    """ Marker interface to detect frontpage
    """

class IOperunSettings(Interface):
    """ Global settings stored in the configuration registry and obtainable via plone.registry.
    """

class IOperunUnique(Interface):
    """Marker interface for classes with only one instance
    """