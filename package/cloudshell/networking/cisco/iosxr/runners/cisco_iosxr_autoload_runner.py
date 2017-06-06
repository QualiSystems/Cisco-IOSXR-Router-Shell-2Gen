#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.networking.cisco.iosxr.snmp.cisco_snmp_handler import CiscoIOSXRSnmpHandler
from cloudshell.networking.cisco.runners.cisco_autoload_runner import CiscoAutoloadRunner


class CiscoIOSXRAutoloadRunner(CiscoAutoloadRunner):
    def __init__(self, cli, logger, resource_config, api):
        super(CiscoIOSXRAutoloadRunner, self).__init__(cli, logger, resource_config, api)

    @property
    def snmp_handler(self):
        return CiscoIOSXRSnmpHandler(self._cli, self.resource_config, self._logger, self._api)
