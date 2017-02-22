#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.devices.runners.state_runner import StateRunner
from cloudshell.networking.cisco.cli.cisco_cli_handler import CiscoCliHandler
from cloudshell.networking.cisco.iosxr.cli.cisco_iosxr_cli_handler import CiscoIOSXRCliHandler
from cloudshell.networking.cisco.runners.cisco_state_runner import CiscoStateRunner


class CiscoIOSXRStateRunner(CiscoStateRunner):
    def __init__(self, cli, logger, api, resource_config):
        """

        :param cli:
        :param logger:
        :param api:
        :param resource_config:
        """

        super(CiscoIOSXRStateRunner, self).__init__(cli, logger, api, resource_config)

    @property
    def cli_handler(self):
        return CiscoIOSXRCliHandler(self.cli, self.resource_config, self._logger, self.api)
