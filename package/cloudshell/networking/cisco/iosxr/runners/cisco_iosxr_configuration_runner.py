from cloudshell.networking.cisco.runners.cisco_configuration_runner import CiscoConfigurationRunner


class CiscoIOSXRConfigurationRunner(CiscoConfigurationRunner):

    @property
    def restore_flow(self):
        return CiscoIOSXRRestoreFlow(cli_handler=self.cli_handler, logger=self._logger)

    @property
    def file_system(self):
        return "bootflash:"
