# -*- coding: utf-8 -*-
from collective import dexteritytextindexer
from operun.crm import MessageFactory as _
from operun.crm.config import ACCOUNT_TYPES
from plone import api
from plone.app.textfield import RichText
from plone.app.vocabularies.catalog import CatalogSource
from plone.dexterity.content import Container
from plone.directives import form
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from z3c.form import validator
from z3c.relationfield.schema import RelationChoice
from zope import schema

import zope.component
import zope.interface


@form.validator()
class IAccount(model.Schema):
    """
    Account Content Type
    """

    title = schema.TextLine(
        title=_(u'Display Name'),
        required=True,
    )

    type = schema.Choice(
        title=_(u'Account Type'),
        vocabulary=ACCOUNT_TYPES,
        required=False,
        default=u'customer',
    )

    logo = NamedBlobImage(
        title=_(u'Company Logo'),
        description=_(u'Please upload an image'),
        required=False,
    )

    ceo = schema.TextLine(
        title=_(u'CEO'),
        required=False,
    )

    email = schema.TextLine(
        title=_(u'E-Mail'),
        required=False,
    )

    phone = schema.TextLine(
        title=_(u'Phone'),
        required=False,
    )

    fax = schema.TextLine(
        title=_(u'Fax'),
        required=False,
    )

    website = schema.TextLine(
        title=_(u'Website'),
        required=False,
    )

    project_reference = schema.TextLine(
        title=_(u'Project Reference'),
        description=_(u'A link to a Trac or Redmine project.'),
        required=False,
    )

    # Address

    form.fieldset('address',
                  label=_(u'Address'),
                  fields=['address', 'zip', 'city', ])

    address = schema.TextLine(
        title=_(u'Address'),
        required=False,
    )

    zip = schema.TextLine(
        title=_(u'ZIP'),
        required=False,
    )

    city = schema.TextLine(
        title=_(u'City'),
        required=False,
    )

    # Billing

    form.fieldset('billing',
                  label=_(u'Billing'),
                  fields=['billing_email', 'billing_contact', ])

    billing_email = schema.TextLine(
        title=_(u'Billing E-Mail'),
        required=False,
    )

    billing_contact = RelationChoice(
        title=_(u'Billing Contact'),
        source=CatalogSource(portal_type='Contact'),
        required=False,
    )

    # Notes

    form.fieldset('notes',
                  label=_(u'Notes'),
                  fields=['text', ])

    dexteritytextindexer.searchable('text')

    text = RichText(
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
        if context_portal_type == 'Accounts':
            results = api.content.find(portal_type='Account', Title=value)  # noqa
            if results:
                raise zope.interface.Invalid(
                    _(u'account_title_form_validator_message',
                      default=u'Display Name not unique!')
                )
            else:
                return True
        else:
            return True


validator.WidgetValidatorDiscriminators(TitleValidator, field=IAccount['title'])  # noqa
zope.component.provideAdapter(TitleValidator)


class Account(Container):
    """
    Account class
    """
