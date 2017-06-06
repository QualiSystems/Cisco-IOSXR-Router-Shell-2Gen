#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.networking.cisco.iosxr.cli.cisco_iosxr_cli_handler import CiscoIOSXRCliHandler
from cloudshell.networking.cisco.runners.cisco_firmware_runner import CiscoFirmwareRunner


class CiscoIOSXRFirmwareRunner(CiscoFirmwareRunner):
    RELOAD_TIMEOUT = 500

    def __init__(self, cli, logger, resource_config, api):
        """Handle firmware upgrade process

            :param CLI cli: Cli object
            :param qs_logger logger: logger
            :param CloudShellAPISession api: cloudshell api object
            :param GenericNetworkingResource resource_config:
            """
        super(CiscoIOSXRFirmwareRunner, self).__init__(cli, logger, resource_config, api)

    @property
    def cli_handler(self):
        return CiscoIOSXRCliHandler(self.cli, self.resource_config, self._logger, self.api)
