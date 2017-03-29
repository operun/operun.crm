# -*- coding: utf-8 -*-
from operun.crm import MessageFactory as _
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


ACCOUNT_TYPES = SimpleVocabulary(
    [SimpleTerm(value=u'customer', title=_(u'Customer')),
     SimpleTerm(value=u'vendor', title=_(u'Vendor')),
     SimpleTerm(value=u'partner', title=_(u'Partner')),
     SimpleTerm(value=u'prospect', title=_(u'Prospect'))]
    )
