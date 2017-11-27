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

from shaddock.drivers.docker.api import DockerApi
from docker import errors as docker_errors
import sys


class Container(object):
    """Instance a defined container

    This class instance a Docker container depending on its
    name and model definition.
    The basics Docker methods are implemented as well as a
    Shaddock's specific one that return the information of
    the concerned container.

    Shaddock keep no tracks of any Container ID and rely on no
    databases. THe containers are retrieve from their names.
    """

    def __init__(self, svc_cfg, containers_all=None):
        self.cfg = svc_cfg
        self.docker_client = None
        if containers_all is None:
            docker_api = DockerApi(self.cfg['api_cfg'])
            self.docker_api = docker_api.connect()
            self.docker_client = self.docker_api.containers
        self.info = self._get_info(containers_all)

    def create(self):
        """Returns (dict):

        A dictionary with an image 'Id' key and a 'Warnings' key.
        """
        print('Creating container: {}'.format(self.cfg['name']))
        create = self.docker_client.create(
            image=self.cfg['image'],
            name=self.cfg['service_name'],
            ports=self.cfg.get('ports'),
            environment=self.cfg.get('env'),
            volumes=self.cfg.get('volumes'),
            hostname=self.cfg['name'],
            command=self.cfg.get('command'),
            detach=self.cfg.get('detach', True),
            stdin_open=self.cfg.get('stdin_open', False),
            tty=self.cfg.get('tty', False),
            mem_limit=self.cfg.get('mem_limit'),
            dns=self.cfg.get('dns'),
            volumes_from=self.cfg.get('volumes_from'),
            network_disabled=self.cfg.get('network_disabled', False),
            entrypoint=self.cfg.get('entrypoint'),
            user=self.cfg.get('user'),
            cpu_shares=self.cfg.get('cpu_shares'),
            working_dir=self.cfg.get('working_dir'),
            domainname=self.cfg.get('domainname'),
            memswap_limit=self.cfg.get('memswap_limit'),
            cpuset=self.cfg.get('cpuset'),
            host_config=self.cfg.get('host_config'),
            mac_address=self.cfg.get('mac_address'),
            labels=self.cfg.get('labels'),
            volume_driver=self.cfg.get('volume_driver'),
            stop_signal=self.cfg.get('stop_signal'),
            networking_config=self.cfg.get('networking_config')
            # For future release of Docker-py:
            #
            # mac_address=self.cfg.get('mac_address'),
            # labels=self.cfg.get('labels'),
            # volume_driver=self.cfg.get('volume_driver'),
            # stop_signal=self.cfg.get('stop_signal'),
            # networking_config=self.cfg.get('networking_config'),
            # healthcheck=self.cfg.get('healthcheck')
            )
        return create['id']

    def start(self):
        """Returns (dict):

        A dictionary with an image 'Id' key and a 'Warnings' key.
        """
        try:
            print('Starting container: {}'.format(self.cfg['name']))
            start = self.docker_client.run(
                name=self.cfg['name'],
                image=self.cfg['image'],
                command=self.cfg.get('command'),
                cap_add=self.cfg.get('cap_drop'),
                cap_drop=self.cfg.get('cap_add'),
                cpu_count=self.cfg.get('cpu_count'),
                cpu_percent=self.cfg.get('cpu_percent'),
                detach=self.cfg.get('detach', True),
                devices=self.cfg.get('devices'),
                privileged=self.cfg.get('privileged'),
                network_mode=self.cfg.get('network_mode', 'bridge'),
                network=self.cfg.get('network'),
                ports=self.cfg.get('ports'),
                lxc_conf=self.cfg.get('lxc_conf'),
                publish_all_ports=self.cfg.get('publish_all_ports'),
                links=self.cfg.get('links'),
                dns=self.cfg.get('dns'),
                dns_search=self.cfg.get('dns_search'),
                volumes_from=self.cfg.get('volumes_from'),
                restart_policy=self.cfg.get('restart_policy'),
                extra_hosts=self.cfg.get('extra_hosts'),
                read_only=self.cfg.get('read_only'),
                pid_mode=self.cfg.get('pid_mode'),
                ipc_mode=self.cfg.get('ipc_mode'),
                security_opt=self.cfg.get('security_opt'),
                ulimits=self.cfg.get('ulimits'),
                working_dir=self.cfg.get('working_dir'),
                )
        except docker_errors.APIError:
            print('Container {} is already running'.format(self.cfg['name']))
            return self.cfg['name']

        return start

    def stop(self):
        c = self.info.get('Container')
        if c is not None:
            print('Stopping container: {}'.format(self.cfg['name']))
            return c.stop()

    def remove(self):
        self.stop()
        c = self.info.get('Container')
        if c is not None:
            print('Removing container: {}'.format(self.cfg['name']))
            try:
                c.remove()
            except docker_errors.NotFound:
                print('Container {} does not exist'.format(self.cfg['name']))
                return True

    def restart(self):
        self.docker_client.restart(self.info['Id'])

    def return_logs(self):
        if self.cfg['image'] is not None:
            # "Fix" in order to not use the stream generator in Python2
            c = self.info.get('Container')
            if sys.version_info > (3, 0):
                try:
                    for line in c.logs(stderr=True,
                                       stdout=True,
                                       timestamps=True,
                                       stream=True,
                                       ):
                        print(line.decode('utf-8').rstrip())
                except (KeyboardInterrupt, SystemExit):
                    return True
            else:
                line = c.logs(stderr=True,
                              stdout=True,
                              timestamps=False,
                              stream=False)
                print(line)

    def _get_info(self, containers_all=None):
        info = {}
        if containers_all is None:
            containers_all = self.docker_client.list(all=True)
        try:
            container = [c for c in containers_all
                         if (c.name in self.cfg['service_name'])][0]

            api = DockerApi(self.cfg['api_cfg'], 'lowlevelapi')
            api = api.connect()
            infos = api.inspect_container(container.id)

            info['Container'] = container
            info['Id'] = container.id
            info['Ip'] = infos['NetworkSettings']['IPAddress']
            info['State'] = container.status

        except IndexError:
            # Container is not running
            info = {}
        return info
