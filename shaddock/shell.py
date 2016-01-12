#!/usr/bin/env python
# Copyright (c) 2013 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
from cliff.app import App
from cliff.commandmanager import CommandManager
from cliff.help import HelpAction
import shaddock.frontend
import logging
import os
import sys


class ShaddockShell(App):

    log = logging.getLogger(__name__)

    def __init__(self):
        super(ShaddockShell, self).__init__(
            description='Shaddock shell',
            version='0.3.2',
            command_manager=CommandManager('shaddock.cli'))
        self._set_shell_commands(self._get_commands())

    def configure_logging(self):
        super(ShaddockShell, self).configure_logging()
        logging.getLogger('iso8601').setLevel(logging.WARNING)
        if self.options.verbose_level <= 1:
            logging.getLogger('requests').setLevel(logging.WARNING)

    def env(self, *args, **kwargs):
        """Returns the first environment variable set.

        If all are empty, defaults to '' or keyword arg `default`.
        """
        for arg in args:
            value = os.environ.get(arg)
            if value:
                return value
        return kwargs.get('default', '')

    def build_option_parser(self, description, version,
                            argparse_kwargs=None):
        """Return an argparse option parser for this application.

        Subclasses may override this method to extend
        the parser with more global options.

        :param description: full description of the application
        :paramtype description: str
        :param version: version number for the application
        :paramtype version: str
        :param argparse_kwargs: extra keyword argument passed to the
                                ArgumentParser constructor
        :paramtype extra_kwargs: dict
        """
        argparse_kwargs = argparse_kwargs or {}
        parser = argparse.ArgumentParser(
            description=description,
            add_help=False,
            **argparse_kwargs
        )
        parser.add_argument(
            '--version',
            action='version',
            version='%(prog)s {0}'.format(version),
            help='Show program\'s version number and exit.'
        )
        parser.add_argument(
            '-v', '--verbose',
            action='count',
            dest='verbose_level',
            default=self.DEFAULT_VERBOSE_LEVEL,
            help='Increase verbosity of output. Can be repeated.',
        )
        parser.add_argument(
            '--log-file',
            action='store',
            default=None,
            help='Specify a file to log output. Disabled by default.',
        )
        parser.add_argument(
            '-q', '--quiet',
            action='store_const',
            dest='verbose_level',
            const=0,
            help='Suppress output except warnings and errors.',
        )
        parser.add_argument(
            '-h', '--help',
            action=HelpAction,
            nargs=0,
            default=self,  # tricky
            help="Show this help message and exit.",
        )
        parser.add_argument(
            '--debug',
            default=False,
            action='store_true',
            help='Show tracebacks on errors.',
        )
        parser.add_argument(
            '-H', '--host',
            action='store',
            dest='docker_host',
            default=self.env('DOCKER_HOST',
                             default='unix://var/run/docker.sock'),
            help='IP/hostname to the Docker API.  (Env: DOCKER_HOST)'
        )
        parser.add_argument(
            '--tlscert',
            action='store',
            dest='docker_cert_path',
            default=self.env('DOCKER_CERT_PATH',
                             default=None),
            help='Path to TLS certificate file.  (Env: DOCKER_CERT_PATH)'
        )
        parser.add_argument(
            '--tlskey',
            action='store',
            dest='docker_key_path',
            default=self.env('DOCKER_KEY_PATH',
                             default=None),
            help='Path to TLS key file.  (Env: DOCKER_KEY_PATH)'
        )
        parser.add_argument(
            '--tlscacert',
            action='store',
            dest='docker_cacert_path',
            default=self.env('DOCKER_CACERT_PATH',
                             default=None),
            help='Trust only remotes providing a certificate signed by the'
                 'CA given here.  (Env: DOCKER_CACERT_PATH)'
        )
        parser.add_argument(
            '--tlsverify',
            action='store',
            dest='docker_tls_verify',
            default=self.env('DOCKER_TLS_VERIFY',
                             default=False),
            help='Use TLS and verify the remote.  (Env: DOCKER_TLS_VERIFY)'
        )
        parser.add_argument(
            '--tls',
            action='store_true',
            dest='docker_tls',
            default=self.env('DOCKER_TLS',
                             default=False),
            help='Use TLS; implied by tls-verify flags.  (Env: DOCKER_TLS)'
        )
        parser.add_argument(
            '--boot2docker',
            action='store_true',
            dest='docker_boot2docker',
            default=self.env('DOCKER_BOOT2DOCKER',
                             default=False),
            help='Use Boot2Docker TLS conf.  (Env: DOCKER_BOOT2DOCKER) \n'
                 'You should first:\n'
                 '\"eval $(sudo docker-machine env machine_name)\"'
        )
        parser.add_argument(
            '--docker-version',
            action='store',
            dest='docker_version',
            default=self.env('DOCKER_VERSION',
                             default='1.12'),
            help='Docker API version number (Env: DOCKER_VERSION)'
        )
        parser.add_argument(
            '-f', '--template-file',
            action='store',
            dest='template_file',
            default=self.env('TEMPLATE_FILE',
                             default=None),
            help='Template file to use. (Env: TEMPLATE_FILE)'
        )
        parser.add_argument(
            '-d', '--images-dir',
            action='store',
            dest='images_dir',
            default=self.env('IMAGES_DIR',
                             default=None),
            help=('Directory to build Docker images from.'
                  '(Env: IMAGES_DIR)')
        )
        return parser

    def initialize_app(self, argv):
        self._clear_shell_commands()
        self._set_shell_commands(self._get_commands())

    def _set_shell_commands(self, cmds_dict):
        for k, v in cmds_dict.items():
            self.command_manager.add_command(k, v)

    @staticmethod
    def _get_commands():
        return {
            'build': shaddock.frontend.Build,
            'create': shaddock.frontend.Create,
            'start': shaddock.frontend.Start,
            'logs': shaddock.frontend.Logs,
            'stop': shaddock.frontend.Stop,
            'restart': shaddock.frontend.Restart,
            'remove': shaddock.frontend.Remove,
            'ps': shaddock.frontend.List,
            'info': shaddock.frontend.Show,
            'pull': shaddock.frontend.Pull
        }

    def _clear_shell_commands(self):
        exclude_cmds = ['help', 'complete']

        cmds = self.command_manager.commands.copy()
        for k, v in cmds.items():
            if k not in exclude_cmds:
                self.command_manager.commands.pop(k)

    def prepare_to_run_command(self, cmd):
        self.log.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.log.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.log.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    return ShaddockShell().run(argv)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
