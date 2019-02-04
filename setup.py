# -*- coding: utf-8 -*-
"""Installer for the operun.crm package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='operun.crm',
    version='2.3.0',
    description="The operun CRM webapp project.",
    long_description=long_description,
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.1",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone',
    author='Jesse Stippel',
    author_email='jesse.stippel@operun.de',
    url='https://pypi.python.org/pypi/operun.crm',
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['operun'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'z3c.jbot',
        'plone.api',
        'setuptools',
        'vobject',
        'collective.dexteritytextindexer',
        'Products.GenericSetup>=1.8.2',
        'plone.app.registry',
        'plone.app.relationfield',
        'plone.app.dexterity [relations]',
        'plone.formwidget.namedfile',
        'plone.formwidget.contenttree',
        'plone.directives.form',
        'plone.namedfile [blobs]',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            'plone.testing>=5.0.0',
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
