# -*- coding: utf-8 -*-
from operun.crm import MessageFactory as _
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


ACCOUNT_TYPES = SimpleVocabulary(
    [SimpleTerm(value=u'contact', title=_(u'Contact')),
     SimpleTerm(value=u'employee', title=_(u'Employee')),
     SimpleTerm(value=u'lead', title=_(u'Lead')),
     SimpleTerm(value=u'customer', title=_(u'Customer')),
     SimpleTerm(value=u'vendor', title=_(u'Vendor'))]
)
