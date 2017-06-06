from cloudshell.networking.cisco.iosxr.cli.cisco_iosxr_cli_handler import CiscoIOSXRCliHandler
from cloudshell.networking.cisco.iosxr.flows.cisco_iosxr_restore_flow import CiscoIOSXRRestoreFlow
from cloudshell.networking.cisco.runners.cisco_configuration_runner import CiscoConfigurationRunner


class CiscoIOSXRConfigurationRunner(CiscoConfigurationRunner):

    @property
    def cli_handler(self):
        """ CLI Handler property
        :return: CLI handler
        """
        return CiscoIOSXRCliHandler(self._cli, self.resource_config, self._logger, self._api)

    @property
    def restore_flow(self):
        return CiscoIOSXRRestoreFlow(cli_handler=self.cli_handler, logger=self._logger)

    @property
    def file_system(self):
        return "bootflash:"
