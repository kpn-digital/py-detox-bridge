#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pkgversion import list_requirements, pep440_version, write_setup_py
from setuptools import find_packages

write_setup_py(
    name='detox-bridge',
    version=pep440_version(),
    description="A python bridge to the detox greybox testing library",
    long_description=open('README.rst').read(),
    author="Jan-Eric Duden",
    author_email='jan-eric.duden@kpn.com',
    url='ssh://git@github.com:kpn-digital/py-detox-bridge.git',
    install_requires=list_requirements('requirements/requirements-base.txt'),
    packages=find_packages(exclude=['tests*', 'detox']),
    tests_require=['tox'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
