#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.devices.runners.run_command_runner import RunCommandRunner
from cloudshell.networking.cisco.cli.cisco_cli_handler import CiscoCliHandler
from cloudshell.networking.cisco.iosxr.cli.cisco_iosxr_cli_handler import CiscoIOSXRCliHandler
from cloudshell.networking.cisco.runners.cisco_run_command_runner import CiscoRunCommandRunner


class CiscoIOSXRRunCommandRunner(CiscoRunCommandRunner):
    def __init__(self, cli, resource_config, logger, api):
        """Create CiscoRunCommandOperations

            :param context: command context
            :param api: cloudshell api object
            :param cli: CLI object
            :param logger: QsLogger object
            :return:
            """
        super(CiscoIOSXRRunCommandRunner, self).__init__(cli, resource_config, logger, api)

    @property
    def cli_handler(self):
        return CiscoIOSXRCliHandler(self.cli, self.resource_config, self._logger, self.api)
