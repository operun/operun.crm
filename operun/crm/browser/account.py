from plone.memoize.view import memoize

from zope.component import getMultiAdapter

from Acquisition import aq_inner

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

from operun.crm import MessageFactory as _


class AccountView(BrowserView):

    template = ViewPageTemplateFile('templates/account.pt')

    def __call__(self):
        """ custom view for account content type
        """

        return self.template()