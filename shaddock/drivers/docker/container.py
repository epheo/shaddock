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

    def __init__(self, name, svc_cfg, infos=None):
        self.name = name
        self.cfg = svc_cfg
        if infos is None:
            docker_api = DockerApi(self.cfg['api_cfg'])
            self.docker_client = docker_api.connect()
        self.info = self._get_info(infos)
        self.info = {}

    def create(self):
        """Returns (dict):

        A dictionary with an image 'Id' key and a 'Warnings' key.
        """
        print('Creating container: {}'.format(self.name))
        create = self.docker_client.create_container(
            image=self.cfg['image'],
            name=self.name,
            ports=self.cfg.get('ports'),
            environment=self.cfg.get('env'),
            volumes=self.cfg.get('volumes'),
            hostname=self.name,
            command=self.cfg.get('command'),
            detach=self.cfg.get('detach', False),
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
        create = create['Id']
        return create

    def start(self):
        """Returns (dict):

        A dictionary with an image 'Id' key and a 'Warnings' key.
        """
        if self.info.get('Id') is None:
            self.info['Id'] = self.create()
        print('Starting container: {}'.format(self.name))
        start = self.docker_client.start(
            container=self.info['Id'],
            binds=self.cfg.get('binds'),
            port_bindings=self.cfg.get('ports_bindings'),
            privileged=self.cfg.get('privileged'),
            network_mode=self.cfg.get('network_mode', 'bridge'),
            lxc_conf=self.cfg.get('lxc_conf'),
            publish_all_ports=self.cfg.get('publish_all_ports'),
            links=self.cfg.get('links'),
            dns=self.cfg.get('dns'),
            dns_search=self.cfg.get('dns_search'),
            volumes_from=self.cfg.get('volumes_from'),
            restart_policy=self.cfg.get('restart_policy'),
            cap_add=self.cfg.get('cap_add'),
            cap_drop=self.cfg.get('cap_drop'),
            devices=self.cfg.get('devices'),
            extra_hosts=self.cfg.get('extra_hosts'),
            read_only=self.cfg.get('read_only'),
            pid_mode=self.cfg.get('pid_mode'),
            ipc_mode=self.cfg.get('ipc_mode'),
            security_opt=self.cfg.get('security_opt'),
            ulimits=self.cfg.get('ulimits'))
        return start

    def stop(self):
        if self.info.get('Id') is not None:
            print('Stopping container: {}'.format(self.name))
            self.docker_client.stop(self.info['Id'])

    def remove(self):
        self.stop()
        if self.info.get('Id') is not None:
            print('Removing container: {}'.format(self.name))
            self.docker_client.remove_container(self.info['Id'])

    def restart(self):
        self.docker_client.restart(self.info['Id'])

    def return_logs(self):
        if self.cfg['image'] is not None:

            # "Fix" in order to not use the stream generator in Python2
            # if sys.version_info > (3, 0):
            #     try:
            #         for line in self.docker_api.logs(
            #             container=self.id,
            #             stderr=True,
            #             stdout=True,
            #             timestamps=False,
            #             stream=True
            #             ):
            #             print(line.decode('utf-8').rstrip())
            #     except (KeyboardInterrupt, SystemExit):
            #         return True
            # else:
                line = self.docker_api.logs(container=self.id,
                                            stderr=True,
                                            stdout=True,
                                            timestamps=False,
                                            stream=False)
                print(line)

    def _get_info(self, containers_info=None):
        if containers_info is None:
            containers_info = self.docker_client.containers(all=True)
        try:
            # One item contains "Names": ["/realname"]
            info = [item for item in containers_info
                    if ("/" + self.name == str(
                        item['Names'][0]))][0]

            info['Ip'] = None
        except IndexError:
            # Container is not running
            info = {}
        return info
