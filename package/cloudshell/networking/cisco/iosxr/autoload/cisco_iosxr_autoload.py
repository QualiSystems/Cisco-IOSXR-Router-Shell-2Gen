from cloudshell.networking.cisco.autoload.cisco_generic_snmp_autoload import CiscoGenericSNMPAutoload
from cloudshell.networking.cisco.autoload.snmp_if_table import SnmpIfTable
from cloudshell.networking.cisco.iosxr.autoload.cisco_iosxr_entity_table import CiscoIOSXREntityTable


class CiscoIOSXRAutoload(CiscoGenericSNMPAutoload):

    def _load_snmp_tables(self):
        """ Load all cisco required snmp tables

        :return:
        """

        self.logger.info('Start loading MIB tables:')
        self.if_table = SnmpIfTable(snmp_handler=self.snmp_handler, logger=self.logger)
        self.logger.info('{0} table loaded'.format(self.IF_ENTITY))
        self.cisco_entity = CiscoIOSXREntityTable(self.snmp_handler, self.logger, self.if_table)
        self.entity_table = self.cisco_entity.get_entity_table()
        self.logger.info('Entity table loaded')

        self.logger.info('MIB Tables loaded successfully')
