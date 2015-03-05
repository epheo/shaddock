#!/usr/bin/env python

#    Copyright (C) 2014 Thibaut Lapierre <root@epheo.eu>. All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from setuptools import setup, find_packages

requirements = ['docker-py',
                'PyYAML>=3.1.0',
                'argparse',
                'panama-template'
                ]
                
testrequirements = ['nose']

setup(
    name='panama',
    description='Easily deploy an OpenStack platform in Docker Containers',
    author='Thibaut Lapierre',
    author_email='root@epheo.eu',
    url='https://github.com/Epheo/panama',
    # download_url='https://github.com/Epheo/panama/archive/master.zip',
    # setup_requires=['setuptools-markdown'],
    long_description_markdown_filename='README.md',
    license='Apache Software License',
    version='0.0.5',
    entry_points={'console_scripts': [
            'panama = panama:__main__'
        ]},
    packages=find_packages(),
    data_files=[('/etc/', ['conf/panama.conf'])],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: OpenStack',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
    ],
)
