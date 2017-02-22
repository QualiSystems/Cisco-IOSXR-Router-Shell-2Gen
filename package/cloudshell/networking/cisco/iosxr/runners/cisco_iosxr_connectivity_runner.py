#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.networking.cisco.iosxr.cli.cisco_iosxr_cli_handler import CiscoIOSXRCliHandler
from cloudshell.networking.cisco.runners.cisco_connectivity_runner import CiscoConnectivityRunner


class CiscoIOSXRConnectivityRunner(CiscoConnectivityRunner):
    def __init__(self, cli, logger, api, resource_config):
        """ Handle add/remove vlan flows

            :param cli:
            :param logger:
            :param api:
            :param resource_config:
            """
        super(CiscoIOSXRConnectivityRunner, self).__init__(cli, logger, api, resource_config)

    @property
    def cli_handler(self):
        return CiscoIOSXRCliHandler(self.cli, self.resource_config, self._logger, self.api)

    # ToDo left as reminder for future connectivity implementation
    # @property
    # def add_vlan_flow(self):
    #     return CiscoAddVlanFlow(self.cli_handler, self._logger)
    #
    # @property
    # def remove_vlan_flow(self):
    #     return CiscoRemoveVlanFlow(self.cli_handler, self._logger)
