# -*- coding: utf-8 -*-
from zope.interface import Interface


class IIsFrontpage(Interface):
    """
    Marker interface to detect frontpage
    """


class IOperunSettings(Interface):
    """
    Global settings stored in the configuration registry
    and obtainable via plone.registry.
    """


class IOperunUnique(Interface):
    """
    Marker interface for classes with only one instance
    """
