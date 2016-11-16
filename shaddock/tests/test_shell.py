# -*- coding: utf-8 -*-
# Copyright 2013 Shaddock org
# All Rights Reserved.
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

import argparse
import mock
import os
from shaddock import exc
from shaddock import shell as shaddock_shell
import six
import sys
import traceback
import unittest
import yaml


TEMPLATE_FILE = ''
IMAGE_DIR = ''
MODEL = ''


class ShellTest(unittest.TestCase):

    def shell(self, argstr, exitcodes=(0,)):
        orig = sys.stdout
        orig_stderr = sys.stderr
        try:
            sys.stdout = six.StringIO()
            sys.stderr = six.StringIO()
            _shell = shaddock_shell.OpenStackImagesShell()
            _shell.main(argstr.split())
        except SystemExit:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.assertIn(exc_value.code, exitcodes)
        finally:
            stdout = sys.stdout.getvalue()
            sys.stdout.close()
            sys.stdout = orig
            stderr = sys.stderr.getvalue()
            sys.stderr.close()
            sys.stderr = orig_stderr
        return (stdout, stderr)

    def test_help_unknown_command(self):
        shell = shaddock_shell.OpenStackImagesShell()
        argstr = '--on 2 help foofoo'
        self.assertRaises(exc.CommandError, shell.main, argstr.split())

    @mock.patch('sys.stdout', six.StringIO())
    @mock.patch('sys.stderr', six.StringIO())
    @mock.patch('sys.argv', ['shaddock', 'help', 'foofoo'])
    def test_no_stacktrace_when_debug_disabled(self):
        with mock.patch.object(traceback, 'print_exc') as mock_print_exc:
            try:
                shaddock_shell.main()
            except SystemExit:
                pass
            self.assertFalse(mock_print_exc.called)

    @mock.patch('sys.stdout', six.StringIO())
    @mock.patch('sys.stderr', six.StringIO())
    @mock.patch('sys.argv', ['shaddock', 'help', 'foofoo'])
    def test_stacktrace_when_debug_enabled_by_env(self):
        old_environment = os.environ.copy()
        os.environ = {'DEBUG': '1'}
        try:
            with mock.patch.object(traceback, 'print_exc') as mock_print_exc:
                try:
                    shaddock_shell.main()
                except SystemExit:
                    pass
                self.assertTrue(mock_print_exc.called)
        finally:
            os.environ = old_environment

    @mock.patch('sys.stdout', six.StringIO())
    @mock.patch('sys.stderr', six.StringIO())
    @mock.patch('sys.argv', ['shaddock', '--debug', 'help', 'foofoo'])
    def test_stacktrace_when_debug_enabled(self):
        with mock.patch.object(traceback, 'print_exc') as mock_print_exc:
            try:
                shaddock_shell.main()
            except SystemExit:
                pass
            self.assertTrue(mock_print_exc.called)

    def test_help(self):
        shell = shaddock_shell.OpenStackImagesShell()
        argstr = '-h'
        with mock.patch.object(shell) as et_mock:
            actual = shell.main(argstr.split())
            self.assertEqual(0, actual)
            self.assertFalse(et_mock.called)

    def test_blank_call(self):
        shell = shaddock_shell.OpenStackImagesShell()
        with mock.patch.object(shell, '_get_keystone_auth_plugin') as et_mock:
            actual = shell.main('')
            self.assertEqual(0, actual)
            self.assertFalse(et_mock.called)

    def test_help_on_subcommand_error(self):
        self.assertRaises(exc.CommandError, shell,
                          'help bad')

    def test_help_v2_no_schema(self):
        shell = shaddock_shell.OpenStackImagesShell()
        argstr = 'help image-create'
        with mock.patch.object(shell, '_get_keystone_auth_plugin') as et_mock:
            actual = shell.main(argstr.split())
            self.assertEqual(0, actual)
            self.assertNotIn('<unavailable>', actual)
            self.assertFalse(et_mock.called)

        argstr = 'help md-namespace-create'
        with mock.patch.object(shell, '_get_keystone_auth_plugin') as et_mock:
            actual = shell.main(argstr.split())
            self.assertEqual(0, actual)
            self.assertNotIn('<unavailable>', actual)
            self.assertFalse(et_mock.called)

        argstr = 'help md-resource-type-associate'
        with mock.patch.object(shell, '_get_keystone_auth_plugin') as et_mock:
            actual = shell.main(argstr.split())
            self.assertEqual(0, actual)
            self.assertNotIn('<unavailable>', actual)
            self.assertFalse(et_mock.called)

    @mock.patch.object(shaddock_shell.OpenStackImagesShell,
                       '_get_versioned_client')
    def test_cert_and_key_args_interchangeable(self,
                                               mock_versioned_client):
        # make sure --os-cert and --os-key are passed correctly
        args = (''
                '--os-cert mycert '
                '--os-key mykey image-list')
        shell(args)
        assert mock_versioned_client.called
        ((api_version, args), kwargs) = mock_versioned_client.call_args
        self.assertEqual('mycert', args.os_cert)
        self.assertEqual('mykey', args.os_key)

        # make sure we get the same thing with --cert-file and --key-file
        args = (''
                '--cert-file mycertfile '
                '--key-file mykeyfile image-list')
        shaddock_shell = shaddock_shell.OpenStackImagesShell()
        shaddock_shell.main(args.split())
        assert mock_versioned_client.called
        ((api_version, args), kwargs) = mock_versioned_client.call_args
        self.assertEqual('mycertfile', args.os_cert)
        self.assertEqual('mykeyfile', args.os_key)
