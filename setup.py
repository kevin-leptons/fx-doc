#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='fx-doc',
    version='0.1.0.5',
    description='Build reStructuredText to HTML, PDF and text',
    keywords=[
        'build', 'document', 'reStructuredText', 
        'HTML', 'PDF', 'texta'
    ],
    author='Kevin Leptons',
    author_email='kevin.leptons@gmail.com',
    url='https://github.com/kevin-leptons/fx-doc',
    install_requires=[
        'sphinx==1.7.2', 'click==6.7', 'flake8==3.5.0', 'PyYAML==3.12',
        'htmlmin==0.1.12', 'pathlib==1.0.1', 'jsmin==2.2.2',
        'csscompressor==0.9.5', 'Pillow==5.0.0'
    ],
    packages=find_packages(exclude=['test']),
    entry_points={
        'console_scripts': {
            'fx-doc = fx_doc.cli:cli'
        }
    },
    classifiers=[
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
)
