# -*- coding: utf-8 -*-
from operun.crm import MessageFactory as _
from operun.crm.config import PRIORITY_TYPES
from operun.crm.config import STATUS_TYPES
from plone.app.vocabularies.catalog import CatalogSource
from plone.dexterity.content import Item
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from zope import schema


class ITodo(model.Schema):
    """
    Todo Content Type
    """

    task_id = schema.TextLine(
        required=False,
        readonly=True,
    )

    owner = RelationChoice(
        title=_(u'Owner'),
        source=CatalogSource(portal_type='Contact'),
        required=False,
    )

    start_date = schema.Date(
        title=_(u'Start Date'),
        required=False,
    )

    end_date = schema.Date(
        title=_(u'End Date'),
        required=False,
    )

    status = schema.Choice(
        title=_(u'Status'),
        vocabulary=STATUS_TYPES,
        required=True,
        default=u'new',
    )

    priority = schema.Choice(
        title=_(u'Priority'),
        vocabulary=PRIORITY_TYPES,
        required=True,
        default=u'normal',
    )


class Todo(Item):
    """
    Todo class
    """
