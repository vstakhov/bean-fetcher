#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(
        name='bean-fetcher',
        version='0.0.2',
        author="Vsevolod Stakhov",
        author_email="vsevolod@highsecure.ru",
        maintainer="Vsevolod Stakhov",
        maintainer_email="vsevolod@highsecure.ru",
        contact_email="vsevolod@highsecure.ru",
        url='https://bitbucket.org/vstakhov/bean-fetcher',
        packages=find_packages('src'),
        package_dir = {'':'src'},
        scripts=['script/bean-fetcher'],
        license='BSD',
        description='Python beanstalk universal fetcher',
        long_description='Python beanstalk universal fetcher.',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache License',
            'Operating System :: POSIX',
            'Programming Language :: Python',
            ]
    )