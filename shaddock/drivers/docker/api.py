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

import docker

# Possibilities:
#
#   Authenticate server based on public/default CA pool
#       Verify --> tls=True
#       No verify --> tls = tls_config = docker.tls.TLSConfig(verify=False)
#
#   Authenticate server based on given CA
#       tls = tls_config = docker.tls.TLSConfig(ca_cert='/path/to/ca.pem')
#
#   Authenticate with client certificate, do not authenticate server based on given CA
#       tls = tls_config = docker.tls.TLSConfig(
#         client_cert=('/path/to/client-cert.pem', '/path/to/client-key.pem'))
#
#   Authenticate with client certificate, authenticate server based on given CA
#       tls = tls_config = docker.tls.TLSConfig(
#         client_cert=('/path/to/client-cert.pem', '/path/to/client-key.pem'),
#         verify='/path/to/ca.pem')


class DockerApi(object):

    def __init__(self, app_args):
        self.app_args = app_args

        self.docker_host = app_args.docker_host
        self.docker_version = app_args.docker_version

        self.docker_cert_path = app_args.docker_cert_path
        self.docker_key_path = app_args.docker_key_path
        self.docker_cacert_path = app_args.docker_cacert_path
        self.docker_tls_verify = app_args.docker_tls_verify
        self.docker_tls = app_args.docker_tls

        if bool(self.docker_tls) is True:
            pass

    def tls_config(self):
        if bool(self.docker_tls_verify) is True:
            tls_config = docker.tls.TLSConfig(verify=False)

            if self.docker_cacert_path:
                tls_config = docker.tls.TLSConfig(
                    client_cert=('/path/to/client-cert.pem',
                                 '/path/to/client-key.pem'),
                    verify='/path/to/ca.pem')

            if self.docker_cacert_path != 'None':
                tls_config = docker.tls.TLSConfig(
                    client_cert=('/path/to/client-cert.pem', '/path/to/client-key.pem'),
                    verify='/path/to/ca.pem')

        else:
            tls_config = docker.tls.TLSConfig(verify=False)

        return tls_config

        else:
            client = docker.Client(base_url='<https_url>')




        client = docker.Client(base_url='<https_url>', tls=True)