#!/usr/bin/env python

from setuptools import setup, find_packages


with open('readme') as f:
        long_desc = f.read()

setup(
    name='fx-doc',
    version='0.4.0',
    license='MIT',
    description='Build reStructuredText to HTML, PDF and text',
    long_description=long_desc,
    long_description_content_type='text/markdown',
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
        'csscompressor==0.9.5', 'Pillow==5.0.0',
        'Flask==0.12.2', 'gunicorn==19.7.1'
    ],
    packages=find_packages(exclude=['test']),
    entry_points={
        'console_scripts': {
            'fx-doc = fx_doc.cli:cli'
        }
    },
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    include_package_data = True
)
