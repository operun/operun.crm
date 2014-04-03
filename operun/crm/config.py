from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from operun.crm import MessageFactory as _


ACCOUNT_TYPES = SimpleVocabulary(
    [SimpleTerm(value=u'customer', title=_(u'Customer')),
     SimpleTerm(value=u'vendor', title=_(u'Vendor')),
     SimpleTerm(value=u'prospect', title=_(u'Prospect'))]
    )
