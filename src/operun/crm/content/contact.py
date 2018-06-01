# -*- coding: utf-8 -*-
from collective import dexteritytextindexer
from operun.crm import MessageFactory as _
from operun.crm.config import ACCOUNT_TYPES
from plone import api
from plone.app.textfield import RichText
from plone.app.vocabularies.catalog import CatalogSource
from plone.dexterity.content import Item
from plone.directives import form
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from z3c.form import validator
from z3c.relationfield.schema import RelationChoice
from zope import schema

import zope.component
import zope.interface


@form.validator()
class IContact(model.Schema):
    """
    Contact Content Type
    """

    title = schema.TextLine(
        title=_(u'Display Name'),
        required=True,
    )

    firstname = schema.TextLine(
        title=_(u'Firstname'),
        required=True,
    )

    lastname = schema.TextLine(
        title=_(u'Lastname'),
        required=True,
    )

    type = schema.Choice(
        title=_(u'Contact Type'),
        vocabulary=ACCOUNT_TYPES,
        required=False,
        default=u'contact',
    )

    # Job Title

    account = RelationChoice(
        title=_(u'Account'),
        source=CatalogSource(portal_type='Account'),
        required=False,
    )

    # Department

    phone = schema.TextLine(
        title=_(u'Phone'),
        required=False,
    )

    mobile = schema.TextLine(
        title=_(u'Mobile'),
        required=False,
    )

    email = schema.TextLine(
        title=_(u'E-Mail'),
        required=False,
    )

    businesscard = NamedBlobImage(
        title=_(u'Business Card'),
        description=_(u'Please upload an image'),
        required=False,
    )

    dexteritytextindexer.searchable('notes')

    notes = RichText(
        title=_(u'Notes'),
        required=False,
    )


class TitleValidator(validator.SimpleFieldValidator):
    """
    z3c.form validator class for checking title uniqueness.
    """

    def validate(self, value):
        """
        Validate titles.
        """
        super(TitleValidator, self).validate(value)
        context_portal_type = self.context.Type()
        if context_portal_type == 'Contacts':
            results = api.content.find(portal_type='Contact', Title=value)  # noqa
            if results:
                raise zope.interface.Invalid(
                    _(u'contact_title_form_validator_message',
                      default=u'Display Name not unique!')
                )
            else:
                return True
        else:
            return True


validator.WidgetValidatorDiscriminators(TitleValidator, field=IContact['title'])  # noqa
zope.component.provideAdapter(TitleValidator)


class Contact(Item):
    """
    Contact class
    """
