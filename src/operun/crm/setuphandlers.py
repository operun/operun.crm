# -*- coding: utf-8 -*-
from plone import api
from plone import namedfile
from plone.app.textfield.value import RichTextValue
from plone.namedfile.file import NamedBlobImage
from Products.CMFPlone.interfaces import INonInstallable
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.interface import implementer
from zope.intid.interfaces import IIntIds


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'operun.crm:uninstall',
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    _displayed_types()
    _set_mark_special_links()


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def _displayed_types():
    """
    Add Training to displayed types.
    """
    types = api.portal.get_registry_record('plone.displayed_types')
    types = types + ('Accounts', 'Contacts', 'Todos')
    api.portal.set_registry_record('plone.displayed_types', types)


def _set_mark_special_links():
    """
    Removes external link icon.
    """
    api.portal.set_registry_record('plone.mark_special_links', False)


def _create_demo_setup(portal, context):
    """
    Create demo content for operun CRM.
    """

    profile_id = 'operun.crm:demo'
    profile_context = context._getImportContext(profile_id)
    profile_path = profile_context._profile_path
    offer_path = profile_path + '/files/offer.pdf'
    invoice_path = profile_path + '/files/invoice.pdf'
    logo_path = profile_path + '/files/logo.jpg'
    businesscard_path = profile_path + '/files/businesscard.jpg'

    # Setup Contacts
    contacts = api.content.create(
        type='Contacts',
        container=portal,
        id='contacts',
        title=u'Kontakte',
        description=u'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.',  # noqa
    )
    api.content.transition(obj=contacts, transition='publish')

    # Setup Accounts
    accounts = api.content.create(
        type='Accounts',
        container=portal,
        id='accounts',
        title=u'Kunden',
        description=u'Ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.',  # noqa
    )
    api.content.transition(obj=accounts, transition='publish')

    # Create Account
    account = api.content.create(
        type='Account',
        container=accounts,
        id='musterfirma-gmbh',
        title=u'Musterfirma GmbH',
        logo=NamedBlobImage(open(logo_path, 'r').read(), filename=u'logo.jpg'),
        ceo=u'Max Mustermann',
        email=u'musterfirma@domain.com',
        phone=u'+49 89 123456-0',
        fax=u'+49 89 123456-99',
        website=u'https://www.musterfirma.de',
        project_reference=u'https://support.example.com/projects/1000',
        address=u'Musterstraße',
        zip=u'12345',
        city=u'Musterstadt',
        billing_email=u'rechnung@musterfirma.de',
        text=RichTextValue(
            u'Sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores.', 'text/plain', 'text/html'),  # noqa
    )
    api.content.transition(obj=account, transition='publish')

    # RelationValue
    intids = getUtility(IIntIds)

    # Create Contact
    contact = api.content.create(
        type='Contact',
        container=contacts,
        id='max-mustermann',
        title=u'Max Mustermann',
        firstname=u'Max',
        lastname=u'Mustermann',
        account=RelationValue(intids.getId(account)),
        phone=u'+49 89 123456-78',
        mobile=u'+49 170 1234567',
        email=u'max.mustermann@musterfirma.de',
        businesscard=NamedBlobImage(open(businesscard_path, 'r').read(), filename=u'businesscard.jpg'),  # noqa
        notes=RichTextValue(
            u'Sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores.', 'text/plain', 'text/html'),  # noqa
    )
    api.content.transition(obj=contact, transition='publish')

    # Create Invoice & Offer

    invoice = api.content.create(
        type='Invoice',
        container=account,
        id='invoice-2017-04-21',
        title=u'Invoice 2017-04-21',
        description=u'Invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata.',  # noqa
        file=namedfile.NamedBlobFile(
            open(invoice_path, 'r').read(),
            filename=u'invoice.pdf'),
    )
    api.content.transition(obj=invoice, transition='publish')

    offer = api.content.create(
        type='Offer',
        container=account,
        id='offer-2017-04-21',
        title=u'Offer 2017-04-21',
        description=u'Invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata.',  # noqa
        file=namedfile.NamedFile(
            data=open(offer_path, 'r').read(),
            filename=u'offer.pdf'),
    )
    api.content.transition(obj=offer, transition='publish')


def demo(context):
    """
    Run demo content install.
    """
    portal = api.portal.get()
    _create_demo_setup(portal, context)
