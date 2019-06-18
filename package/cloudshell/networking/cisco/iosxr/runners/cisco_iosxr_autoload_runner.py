from cloudshell.networking.cisco.iosxr.flows.cisco_iosxr_autoload_flow import CiscoIOSXRSnmpAutoloadFlow
from cloudshell.networking.cisco.runners.cisco_autoload_runner import CiscoAutoloadRunner


class CiscoIOSXRAutoloadRunner(CiscoAutoloadRunner):

    @property
    def autoload_flow(self):
        return CiscoIOSXRSnmpAutoloadFlow(self.snmp_handler, self._logger)