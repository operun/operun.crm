# -*- coding: utf-8 -*-
from plone import api
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from vcard import generate_vcard


class ContactView(BrowserView):

    template = ViewPageTemplateFile('templates/contact.pt')

    def __call__(self):
        """
        Custom view for contact Content-Type
        """
        if 'download' in self.request:
            self.get_vcard()
        return self.template()

    def get_image(self):
        """
        Get object image.
        """
        context = self.context
        request = self.request
        tag = None
        if context.businesscard:
            images_view = api.content.get_view('images', context, request)
            scale = images_view.scale('businesscard', width=250, height=250, direction='thumbnail')  # noqa
            tag = scale.tag()
        return tag

    def get_vcard(self):
        """
        Get vCard construct.
        """
        import os
        import tempfile
        # Defaults
        context = self.context
        vcard_data = generate_vcard(context)
        firstname = context.firstname
        lastname = context.lastname
        vcard_filename = u'vCard_{0}_{1}.vcf'.format(firstname, lastname)
        # Write
        temp = tempfile.mktemp()
        f = open(temp, 'w')
        f.write(vcard_data)
        f.close()
        data = open(temp).read()
        os.unlink(temp)
        # Header
        R = self.request.response
        R.setHeader('content-type', 'vcard/vcf')
        R.setHeader('content-length', len(data))
        R.setHeader('content-disposition', 'attachment; filename="%s"' % vcard_filename)  # noqa
        return R.write(data)
