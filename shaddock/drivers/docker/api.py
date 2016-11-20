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

from docker.client import Client
from docker.tls import TLSConfig
from docker.utils import kwargs_from_env


class DockerApi(object):
    """An abstraction class to the Docker API

    This class initiate a connection to the Docker API depending
    on the configuration gathered from the model.

     """

    def __init__(self, api_cfg):
        self.api_cfg = api_cfg

    def connect(self):
        url = self.api_cfg.get('url', 'unix://var/run/docker.sock')
        version = self.api_cfg.get('version', '1.12')
        boot2docker = self.api_cfg.get('boot2docker')

        tls_config = self._construct_tlsconfig()
        if boot2docker is True:
            kwargs = kwargs_from_env()
            kwargs['tls'].assert_hostname = False
            client = Client(**kwargs)
        else:
            client = Client(base_url=url,
                            version=str(version),
                            tls=tls_config,
                            timeout=50)
        return client

    def _construct_tlsconfig(self):
        """The Docker tls configuration works as follow:

        Authenticate server based on public/default CA pool
            Verify --> tls=True
            No verify --> tls = tls_config = docker.tls.TLSConfig(verify=False)
           opt: --tls

        Authenticate with client certificate, do not authenticate server based
        on given CA
            tls = tls_config = docker.tls.TLSConfig(
              client_cert=('/path/to/client-cert.pem',
                           '/path/to/client-key.pem'))
           opt: --tls
                --tlscert /path/to/client-cert.pem
                --tlskey /path/to/client-key.pem

        Authenticate server based on given CA
            tls = tls_config = docker.tls.TLSConfig(ca_cert='/path/to/ca.pem')
           opt: --tlsverify
                --tlscacert /path/to/ca.pem

        Authenticate with client certificate, authenticate server based
        on given CA
            tls = tls_config = docker.tls.TLSConfig(
              client_cert=('/path/to/client-cert.pem',
                           '/path/to/client-key.pem'),
              verify='/path/to/ca.pem')
            opt: --tlsverify \
                 --tlscert /path/to/client-cert.pem \
                 --tlskey /path/to/client-key.pem \
                 --tlscacert /path/to/ca.pem
             """

        tls_config = False
        tls = self.api_cfg.get('tls', False)
        cert_path = self.api_cfg.get('cert_path')
        key_path = self.api_cfg.get('key_path')
        tls_verify = self.api_cfg.get('tls_verify', False)
        cacert_path = self.api_cfg.get('cacert_path')

        if tls is True and tls_verify is False:
            if (cert_path is not None) and (key_path is not None):
                print('--tls'
                      '--tlscert /path/to/client-cert.pem'
                      '--tlskey /path/to/client-key.pem')
                tls_config = TLSConfig(client_cert=(cert_path, key_path))
            else:
                tls_config = TLSConfig(verify=False)

        if tls_verify is True:
            if cacert_path is not None:
                if (cert_path is not None) and (
                        key_path is not None):
                    print('--tlsverify'
                          '--tlscert /path/to/client-cert.pem'
                          '--tlskey /path/to/client-key.pem'
                          '--tlscacert /path/to/ca.pem')
                    tls_config = TLSConfig(client_cert=(
                        cert_path,
                        key_path),
                        verify=cacert_path)
                else:
                    print('--tlsverify '
                          '--tlscacert /path/to/ca.pem')
                    tls_config = TLSConfig(ca_cert=cacert_path)
            else:
                raise IndexError("Please specify at least a CA cert with "
                                 "--tlscacert", tls_config)
        return tls_config
