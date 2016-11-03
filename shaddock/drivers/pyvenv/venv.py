#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

import os
import re
import subprocess
import virtualenv

here = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(here)
script_name = os.path.join(base_dir, 'setup.py')

from shaddock import model
import sys

import os
import os.path
from subprocess import Popen
from subprocess import PIPE
import sys
from threading import Thread
from urllib.parse import urlparse
from urllib.request import urlretrieve
import venv

class ExtendedEnvBuilder(venv.EnvBuilder):

    def shell(args=None):
        import argparse
    
        parser = argparse.ArgumentParser(prog=__name__,
                                         description='Creates virtual Python '
                                                     'environments in one or '
                                                     'more target '
                                                     'directories.')
        parser.add_argument('dirs', metavar='ENV_DIR', nargs='+',
                            help='A directory to create the environment in.')
        parser.add_argument('--no-setuptools', default=False,
                            action='store_true', dest='nodist',
                            help="Don't install setuptools or pip in the "
                                 "virtual environment.")
        parser.add_argument('--no-pip', default=False,
                            action='store_true', dest='nopip',
                            help="Don't install pip in the virtual "
                                 "environment.")
        parser.add_argument('--system-site-packages', default=False,
                            action='store_true', dest='system_site',
                            help='Give the virtual environment access to the '
                                 'system site-packages dir.')
        if os.name == 'nt':
            use_symlinks = False
        else:
            use_symlinks = True
        parser.add_argument('--symlinks', default=use_symlinks,
                            action='store_true', dest='symlinks',
                            help='Try to use symlinks rather than copies, '
                                 'when symlinks are not the default for '
                                 'the platform.')
        parser.add_argument('--clear', default=False, action='store_true',
                            dest='clear', help='Delete the contents of the '
                                               'environment directory if it '
                                               'already exists, before '
                                               'environment creation.')
        parser.add_argument('--upgrade', default=False, action='store_true',
                            dest='upgrade', help='Upgrade the environment '
                                               'directory to use this version '
                                               'of Python, assuming Python '
                                               'has been upgraded in-place.')
        parser.add_argument('--verbose', default=False, action='store_true',
                            dest='verbose', help='Display the output '
                                               'from the scripts which '
                                               'install setuptools and pip.')
        options = parser.parse_args(args)
        if options.upgrade and options.clear:
            raise ValueError('you cannot supply --upgrade & --clear together.')
        builder = ExtendedEnvBuilder(system_site_packages=options.system_site,
                                       clear=options.clear,
                                       symlinks=options.symlinks,
                                       upgrade=options.upgrade,
                                       nodist=options.nodist,
                                       nopip=options.nopip,
                                       verbose=options.verbose)
        for d in options.dirs:
            builder.create(d)


class Container(object):
    """
    This builder installs setuptools and pip so that you can pip or
    easy_install other packages into the created environment.

    :param nodist: If True, setuptools and pip are not installed into the
                   created environment.
    :param nopip: If True, pip is not installed into the created
                  environment.
    :param progress: If setuptools or pip are installed, the progress of the
                     installation can be monitored by passing a progress
                     callable. If specified, it is called with two
                     arguments: a string indicating some progress, and a
                     context indicating where the string is coming from.
                     The context argument can have one of three values:
                     'main', indicating that it is called from virtualize()
                     itself, and 'stdout' and 'stderr', which are obtained
                     by reading lines from the output streams of a subprocess
                     which is used to install the app.

                     If a callable is not specified, default progress
                     information is output to sys.stderr.
    """


        self.extra_text   = ""
        self.git_location = "" 


    def __init__(self, service_name, *args, **kwargs):
        self.nodist = kwargs.pop('nodist', False)
        self.nopip = kwargs.pop('nopip', False)
        self.progress = kwargs.pop('progress', None)
        self.verbose = kwargs.pop('verbose', False)

        self.app_args = app_args
        # input_name can ba a tag or a name
        self.input_name = service_name
        self.cfg = model.ContainerConfig(service_name, self.app_args)
        self.tag = self.cfg.tag
        self.name = self.cfg.name

        docker_client = dockerapi.DockerApi(app_args)
        self.docker_api = docker_client.api

        info = self.get_info()
        for attr in info.keys():
            setattr(self, attr, info[attr])
        # self.id = info['id']
        # self.ip = info['ip']
        # self.hostname = info['hostname']
        # self.started = info['started']
        # self.created = info['created']

        super().__init__(*args, **kwargs)

    def create(self):
        print('Creating container: {}'.format(self.name))

        text = virtualenv.create_bootstrap_script(EXTRA_TEXT, python_version='2.7')
        if os.path.exists(script_name):
            f = open(script_name)
            cur_text = f.read()
            f.close()
        else:
            cur_text = ''
        print("Updating %s" % script_name)
        if cur_text == 'text':
            print('No update')
        else:
            print('Script changed; updating...')
            f = open(script_name, 'w')
            f.write(text)
            f.close()

        return c_id

    def start(self):
        return True

    def stop(self):
        return True

    def remove(self):
        return True

    def restart(self):
        return True

    def return_logs(self):
        return True

    def get_info(self):
        info = {}
        info['id'] = None
        info['ip'] = None
        info['hostname'] = None
        info['started'] = False
        info['created'] = False
        info['status'] = 'Not Created'
        containers_list = self.docker_api.containers(all=True)
        if containers_list:
            try:
                # One item contains "Names": ["/realname"]
                c_id, c_status = [(item['Id'], item['Status'])
                                  for item in containers_list
                                  if ("/" + self.name ==
                                      str(item['Names'][0]))][0]
            except IndexError:
                c_id = None
                c_status = 'Not Created'

            if c_id:
                container_info = self.docker_api.inspect_container(c_id)
                config = container_info['Config']
                network = container_info['NetworkSettings']
                info['started'] = container_info['State']['Running']
                info['id'] = c_id
                info['ip'] = network['IPAddress']
                info['hostname'] = config['Hostname']
                if c_status == "":
                    info['status'] = 'Created'
                else:
                    info['status'] = c_status
                info['created'] = True
        return info

    def post_setup(self, context):
        """
        Set up any packages which need to be pre-installed into the
        environment being created.

        :param context: The information for the environment creation request
                        being processed.
        """
        os.environ['VIRTUAL_ENV'] = context.env_dir
        if not self.nodist:
            self.install_setuptools(context)
        # Can't install pip without setuptools
        if not self.nopip and not self.nodist:
            self.install_pip(context)

    def reader(self, stream, context):
        """
        Read lines from a subprocess' output stream and either pass to a progress
        callable (if specified) or write progress information to sys.stderr.
        """
        progress = self.progress
        while True:
            s = stream.readline()
            if not s:
                break
            if progress is not None:
                progress(s, context)
            else:
                if not self.verbose:
                    sys.stderr.write('.')
                else:
                    sys.stderr.write(s.decode('utf-8'))
                sys.stderr.flush()
        stream.close()

    def install_script(self, context, name, url):
        _, _, path, _, _, _ = urlparse(url)
        fn = os.path.split(path)[-1]
        binpath = context.bin_path
        distpath = os.path.join(binpath, fn)
        # Download script into the env's binaries folder
        urlretrieve(url, distpath)
        progress = self.progress
        if self.verbose:
            term = '\n'
        else:
            term = ''
        if progress is not None:
            progress('Installing %s ...%s' % (name, term), 'main')
        else:
            sys.stderr.write('Installing %s ...%s' % (name, term))
            sys.stderr.flush()
        # Install in the env
        args = [context.env_exe, fn]
        p = Popen(args, stdout=PIPE, stderr=PIPE, cwd=binpath)
        t1 = Thread(target=self.reader, args=(p.stdout, 'stdout'))
        t1.start()
        t2 = Thread(target=self.reader, args=(p.stderr, 'stderr'))
        t2.start()
        p.wait()
        t1.join()
        t2.join()
        if progress is not None:
            progress('done.', 'main')
        else:
            sys.stderr.write('done.\n')
        # Clean up - no longer needed
        os.unlink(distpath)

    def install_setuptools(self, context):
        """
        Install setuptools in the environment.

        :param context: The information for the environment creation request
                        being processed.
        """
        url = 'https://bitbucket.org/pypa/setuptools/downloads/ez_setup.py'
        self.install_script(context, 'setuptools', url)
        # clear up the setuptools archive which gets downloaded
        pred = lambda o: o.startswith('setuptools-') and o.endswith('.tar.gz')
        files = filter(pred, os.listdir(context.bin_path))
        for f in files:
            f = os.path.join(context.bin_path, f)
            os.unlink(f)

    def install_pip(self, context):
        """
        Install pip in the environment.

        :param context: The information for the environment creation request
                        being processed.
        """
        url = 'https://raw.github.com/pypa/pip/master/contrib/get-pip.py'
        self.install_script(context, 'pip', url)

