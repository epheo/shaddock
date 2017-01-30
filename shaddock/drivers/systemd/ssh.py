#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright (C) 2014 Thibaut Lapierre <git@epheo.eu>. All Rights Reserved.
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

import paramiko


class SecureShell(object):
    """An abstraction class to an ssh connection.

    This class initiate an ssh connection depending
    on the configuration gathered from the model.

     """

    def __init__(self, api_cfg):
        self.api_cfg = api_cfg.get('systemd')

    def execute(self, command):
        try:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            client.connect(hostname=self.api_cfg.get('hostname', 'localhost'),
                           port=self.api_cfg.get('port'),
                           username=self.api_cfg.get('username'),
                           password=self.api_cfg.get('password'),
                           key_filename=self.api_cfg.get('key_filename'))

            stdin, stdout, stderr = client.exec_command(command)
            print(stdout.read())

        except IndexError:
            print(stderr.read())

        finally:
            client.close()

    def copy(self, source, dest):
        try:
            t = paramiko.Transport((self.api_cfg.get('hostname'),
                                    self.api_cfg.get('port')))
            t.connect(username=self.api_cfg.get('username'),
                      password=self.api_cfg.get('password'))
            sftp = paramiko.SFTPClient.from_transport(t)
            sftp.put(source, dest)

        finally:
            t.close()
