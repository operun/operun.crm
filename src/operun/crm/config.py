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

STATUS_TYPES = SimpleVocabulary(
    [SimpleTerm(value=u'new', title=_(u'New')),
     SimpleTerm(value=u'ongoing', title=_(u'Ongoing')),
     SimpleTerm(value=u'done', title=_(u'Done'))]
)

PRIORITY_TYPES = SimpleVocabulary(
    [SimpleTerm(value=u'low', title=_(u'Low')),
     SimpleTerm(value=u'normal', title=_(u'Normal')),
     SimpleTerm(value=u'high', title=_(u'High'))]
)
