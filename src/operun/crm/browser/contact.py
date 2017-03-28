# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import ldap


class ContactView(BrowserView):

    template = ViewPageTemplateFile('templates/contact.pt')

    # LDAP config
    users = 'ou=users,dc=operun,dc=de'
    groups = 'ou=groups,dc=operun,dc=de'
    admin = 'cn=admin,dc=operun,dc=de'
    server = 'ldap://10.0.0.126'

    # Connect
    con = ldap.initialize(server)
    con.simple_bind_s(admin, '12345')

    # LDAP lists
    available_users = con.search_s(users,
                                   ldap.SCOPE_SUBTREE,
                                   '(objectclass=inetOrgPerson)'
                                   )
    available_groups = con.search_s(groups,
                                    ldap.SCOPE_SUBTREE,
                                    '(objectclass=posixGroup)'
                                    )

    def __call__(self):
        """
        Custom view for contact Content-Type.
        """

        return self.template()

    def modify_user_attribute(self, user=None, attribute=None, new_value=None):
        """
        Modifies an attribute in LDAP.
        """
        if not user:
            user = str(self.context.title)
        mod_attrs = [(ldap.MOD_REPLACE, attribute, new_value)]
        self.con.modify_s('cn={0},{1}'.format(user, self.users), mod_attrs)

    def on_action(self):
        form = self.request.form
        if len(form):
            attr = form['attr']
            newval = form['newval']
            self.modify_user_attribute(attribute=attr, new_value=newval)
