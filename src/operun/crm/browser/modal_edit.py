# -*- coding: utf-8 -*-
from operun.crm import MessageFactory as _
from plone import api
from plone.dexterity.browser import edit
from plone.dexterity.events import EditFinishedEvent
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from z3c.form import interfaces
from zope.event import notify

import logging


logger = logging.getLogger(__name__)


class ModalEditForm(edit.DefaultEditForm):
    """
    Edit only one field at a time. To be used in modals.
    """

    template = ViewPageTemplateFile('templates/modal_edit.pt')

    @button.buttonAndHandler(_(u'Save'), name='save')
    def handleApply(self, action):  # noqa
        # Override widget modes to ignore all other fields
        prefix = 'form.widgets.'
        field_ids = [k.split(prefix)[-1] for k in self.request.form.keys()]
        self.request.set('fields', field_ids)
        # Set all widgets to 'display' to prevent saving data
        self.set_all_widgets_mode(interfaces.DISPLAY_MODE)
        # Change the custom_form_fields to input-mode
        self.set_widgets_mode(field_ids, interfaces.INPUT_MODE)
        # Original code
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(self.success_message, 'info',)  # noqa
        self.request.response.redirect(self.nextURL())
        notify(EditFinishedEvent(self.context))

    def fields_info(self, fields=None):
        """
        Get info about the fields and their modes from the query-string.
        """
        results = []
        if not fields:
            return
        if not isinstance(fields, list):
            fields = [fields]
        sorted_fields = []
        schema_fields = self.fields.keys()
        for fieldname in schema_fields + fields:
            if fieldname not in sorted_fields and fieldname in fields:
                sorted_fields.append(fieldname)
        for fieldname in sorted_fields:
            fieldmode = interfaces.INPUT_MODE
            label = True
            mode = None
            if ':' in fieldname:
                values = fieldname.split(':')
                if len(values) == 2:
                    fieldname, mode = values
                elif len(values) == 3:
                    fieldname, mode, label = values
                    if label.lower() in ['0', 'false', 'no']:
                        label = False
            if mode and mode in [interfaces.INPUT_MODE, interfaces.DISPLAY_MODE, interfaces.HIDDEN_MODE]:  # noqa
                fieldmode = str(mode)
            results.append({
                'fieldname': fieldname,
                'fieldmode': fieldmode,
                'label': label,
            })
        return results

    def get_widget(self, fieldname=None, fieldmode=None, label=True, autofocus=False):  # noqa
        fieldname = fieldname or self.request.get('fieldname')
        fieldmode = fieldmode or self.request.get('fieldmode') or interfaces.INPUT_MODE  # noqa
        field_hooks = {
            'textline-field': 'type=\"text\"',
            'list-field': 'type=\"text\"',
            'richtext-field': 'textarea',
        }
        label = label or self.request.get('label')
        if not fieldname:
            return
        widget = self.find_widget(fieldname)
        if widget:
            widget.mode = fieldmode
            fieldclass = widget.klass
            # Return wrapped or non-wrapped field element
            if not label:
                widget_view = widget.render
            else:
                widget_view = api.content.get_view(
                    'ploneform-render-widget', widget, self.request)
            # Apply autofocus attribute
            if autofocus and fieldclass:
                for key in field_hooks.keys():
                    if key in fieldclass:
                        hook = field_hooks[key]
                        widget_view = widget_view()
                        widget_view = widget_view.replace(hook, hook + ' autofocus=\"\"', 1)  # noqa
                        return widget_view
            return widget_view()

    def set_all_widgets_mode(self, mode):
        for widget in self.widgets.values():
            widget.mode = mode
        group_widgets = [widget for group in self.groups for widget in group.widgets.values()]  # noqa
        for widget in group_widgets:
            widget.mode = mode

    def set_widgets_mode(self, field_ids, mode):
        for field_id in field_ids:
            widget = self.find_widget(field_id)
            if widget:
                widget.mode = mode

    def find_widget(self, field_id):
        """
        Return a widget for any field in the schema and behaviors.
        """
        widget = self.widgets.get(field_id, None)
        if not widget:
            for group in self.groups:
                widget = group.widgets.get(field_id, None)
                if widget:
                    break
        if widget:
            return widget
