#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


import twentiment


setup(
    name='twentiment-api',
    version=twentiment.__version__,
    description='Twitter sentiment analysis tool API',
    long_description=open('README.rst').read(),
    author='Pascal Hartig',
    author_email='phartig@rdrei.net',
    url='https://github.com/passy/twentiment-api',
    packages=['twentiment_api'],
    package_data={'': ['LICENSE', 'README.rst']},
    include_package_data=True,
    install_requires=[
        'flask==0.9'
    ],
    license=open('LICENSE').read(),
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Operating System :: Unix',
        'Topic :: Communications',
        'Topic :: Internet :: WWW/HTTP'
    )
)
