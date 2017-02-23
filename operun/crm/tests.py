import doctest
import unittest

from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite

import operun.crm

OPTION_FLAGS = doctest.NORMALIZE_WHITESPACE | \
    doctest.ELLIPSIS

ptc.setupPloneSite(products=['operun.crm'])


class TestCase(ptc.PloneTestCase):

    class layer(PloneSite):

        @classmethod
        def setUp(cls):
            zcml.load_config('configure.zcml', operun.crm)

        @classmethod
        def tearDown(cls):
            pass


def test_suite():
    return unittest.TestSuite([
        ztc.ZopeDocFileSuite(
            'INTEGRATION.txt',
            package='operun.crm',
            optionflags=OPTION_FLAGS,
            test_class=TestCase
        ),
    ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
