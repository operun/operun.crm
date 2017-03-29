# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from operun.crm.testing import OPERUN_CRM_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that operun.crm is properly installed."""

    layer = OPERUN_CRM_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if operun.crm is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'operun.crm'))

    def test_browserlayer(self):
        """Test that IOperunCrmLayer is registered."""
        from operun.crm.interfaces import (
            IOperunCrmLayer)
        from plone.browserlayer import utils
        self.assertIn(IOperunCrmLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = OPERUN_CRM_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['operun.crm'])

    def test_product_uninstalled(self):
        """Test if operun.crm is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'operun.crm'))

    def test_browserlayer_removed(self):
        """Test that IOperunCrmLayer is removed."""
        from operun.crm.interfaces import \
            IOperunCrmLayer
        from plone.browserlayer import utils
        self.assertNotIn(IOperunCrmLayer, utils.registered_layers())
