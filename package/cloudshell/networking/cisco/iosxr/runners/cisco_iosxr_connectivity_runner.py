#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.networking.cisco.iosxr.cli.cisco_iosxr_cli_handler import CiscoIOSXRCliHandler
from cloudshell.networking.cisco.iosxr.flows.cisco_iosxr_add_vlan_flow import CiscoIOSXRAddVlanFlow
from cloudshell.networking.cisco.iosxr.flows.cisco_iosxr_remove_vlan_flow import CiscoIOSXRRemoveVlanFlow
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

    @property
    def add_vlan_flow(self):
        return CiscoIOSXRAddVlanFlow(self.cli_handler, self._logger)

    @property
    def remove_vlan_flow(self):
        return CiscoIOSXRRemoveVlanFlow(self.cli_handler, self._logger)
