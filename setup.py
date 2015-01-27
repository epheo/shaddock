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

import setuptools
import os

requirements = ['docker-py',
                'PyYAML>=3.1.0',
                'argparse',
                ]
                
testrequirements=['nose', ]

def get_config_files():

    config_files=[
                  ('/etc/octopenstack', ['conf/configuration.yml', 'conf/services.yml']),
                  ]
    config_path = '/etc/octopenstack'
    config_name = 'dockerfiles'

    for dirname, dirnames, filenames in os.walk('dockerfiles'):
        for subdirname in dirnames:
            config_dest_path = ('/etc/octopenstack/%s' % subdirname)
            for dirname, dirnames, filenames in os.walk('dockerfiles/%s' % subdirname):
                config_dir=[]
                for filename in filenames:
                    config_src_path = ('%s/%s' % (dirname, filename))
                    config_dir.append(config_src_path)

            config_file_dir_liste = config_dest_path, config_dir
            config_files.append(config_file_dir_liste)


    return config_files

containers_config=get_config_files()

setuptools.setup(
    name='octopenstack',
    description='Easily deploy an OpenStack platform in Docker Containers',
    author='Thibaut Lapierre',
    author_email='root@epheo.eu',
    url='https://github.com/Epheo/octopenstack',
    download_url='https://github.com/Epheo/octopenstack/archive/master.zip',
    long_description=open("README.md", 'rb').read(),
    packages=setuptools.find_packages(),
    license='Apache Software License',
    version='2014-0.1-dev',
    entry_points={
        'console_scripts': [
            'octopenstack = octopenstack:main'
        ]
    },
    data_files=containers_config,
    install_requires=requirements,
    tests_require=testrequirements,
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
