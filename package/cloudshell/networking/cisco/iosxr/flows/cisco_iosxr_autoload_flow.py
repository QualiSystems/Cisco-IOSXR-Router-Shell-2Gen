from cloudshell.networking.cisco.flows.cisco_autoload_flow import CiscoSnmpAutoloadFlow
from cloudshell.networking.cisco.iosxr.autoload.cisco_iosxr_autoload import CiscoIOSXRAutoload


class CiscoIOSXRSnmpAutoloadFlow(CiscoSnmpAutoloadFlow):
    def execute_flow(self, supported_os, shell_name, shell_type, resource_name):
        with self._snmp_handler.get_snmp_service() as snmp_service:
            cisco_snmp_autoload = CiscoIOSXRAutoload(snmp_service,
                                                     shell_name,
                                                     shell_type,
                                                     resource_name,
                                                     self._logger)
            return cisco_snmp_autoload.discover(supported_os)
