import re

from cloudshell.networking.cisco.autoload.snmp_entity_table import CiscoSNMPEntityTable


class CiscoIOSXREntityTable(CiscoSNMPEntityTable):
    def get_entity_table(self):
        self._entity_table = self._get_entity_table()
        self._filter_lower_bay_containers()
        self._get_sorted_modules_with_ports()
        self._filter_power_port_list()
        return self._entity_table

    def _get_sorted_modules_with_ports(self):
        port_relative_address_dict = {}
        for port in self._port_list:
            port_id = None
            port_if_obj = self.port_mapping.get(port)
            self._logger.debug("Start port {} parent modules id validation".format(port_if_obj.if_name))
            port_parent_ids_match = re.search(r"\d+(/\d+)*$", port_if_obj.if_name, re.IGNORECASE)
            if port_parent_ids_match:
                port_id = port_parent_ids_match.group()

            if port_id:
                port_parent_ids = port_id.rpartition("/")[0]
                if port_parent_ids \
                        and len(port_parent_ids) > 1 \
                        and port_parent_ids in self.relative_address.values():
                    if self._get_module_index_by_relative_path(port_parent_ids) not in self.exclusion_list:
                        port_relative_address_dict[port] = "{}/{}".format(port_parent_ids, self.get_resource_id(port))
                        continue
                    else:
                        self.exclusion_list.append(port)
            parents_list = list(self._get_port_parents(port))[::-1]
            if parents_list:
                if len(parents_list) > 1:
                    if parents_list[1] not in self._module_list:
                        port_parent_id = self._analyze_module(parents_list[1], port_id)
                    else:
                        port_parent_id = self.relative_address.get(parents_list[1])
                    if len(parents_list) > 2:
                        if parents_list[2] not in self._module_list:
                            port_parent_id = self._analyze_module(parents_list[2], port_id)
                        else:
                            port_parent_id = self.relative_address.get(parents_list[2])
                else:
                    port_parent_id = self.relative_address.get(parents_list[0])
            else:
                continue
            if not any([parent_id for parent_id in parents_list[:3] if parent_id in self.exclusion_list]):
                port_relative_address_dict[port] = "{}/{}".format(port_parent_id, self.get_resource_id(port))
            else:
                self.exclusion_list.append(port)
            self._logger.debug("Completed port {} parent modules id validation".format(port_if_obj.if_name))

        self.relative_address.update(port_relative_address_dict)
        module_relative_paths = sorted(self.relative_address, key=self.relative_address.get)
        self._sorted_module_list = [module for module in module_relative_paths if
                                    module in self._module_list and module not in self.exclusion_list]

    def _analyze_module(self, module, port_id=None):
        if module not in self.exclusion_list:
            module_parent_address = self.get_relative_address(module)
            if not module_parent_address:
                self._excluded_models.append(module)
                return

            module_parent_address_list = module_parent_address.split("/")
            if len(module_parent_address_list) > 2:
                module_parent_address = '{0}/{1}'.format(module_parent_address[0], module_parent_address[1])

            module_rel_path = module_parent_address + '/' + self.get_resource_id(module)

            if not port_id.startswith(module_rel_path):
                module_rel_path = self._validate_port_parent_ids(module_rel_path, port_id) \
                                  or module_rel_path

            i = 1
            while module_rel_path in self.relative_address.values():
                i += 1
                module_rel_path = '{0}/{1}'.format(module_parent_address, (int(self.get_resource_id(module)) + i))
            self.relative_address[module] = module_rel_path
            self._module_list.append(module)
            self._logger.debug("Added {0} with relative path {1}".format(self._entity_table[module]["entPhysicalDescr"],
                                                                         module_rel_path))
            return module_rel_path
        else:
            self._excluded_models.append(module)

    def _get_port_parents(self, module_id):
        """
        Retrieve all parent modules for a specific module

        :param module_id:
        :return list: parent modules
        """

        result = []
        parent_id = int(self._entity_table[module_id]['entPhysicalContainedIn'])
        if parent_id > 0 and parent_id in self._entity_table:
            if re.search(r'module', self._entity_table[parent_id]['entPhysicalClass']):
                result.append(parent_id)
                result.extend(self._get_port_parents(parent_id))
            elif re.search(r'chassis', self._entity_table[parent_id]['entPhysicalClass']):
                result.append(parent_id)
                return result
            else:
                result.extend(self._get_port_parents(parent_id))
        else:
            self.exclusion_list.append(module_id)
        return result

    def _validate_port_parent_ids(self, parent_ids, port_ids):
        result = None
        parent_ids_list = parent_ids.split("/")  # ["0", "11"]
        parent_ids_from_port_list = port_ids.split("/")  # ["0", "7", "0", "0"]
        if len(parent_ids_from_port_list) > len(parent_ids_list):  # > 1:
            parent_ids_from_port_list = parent_ids_from_port_list[:len(parent_ids_list)]  # ["0", "7"]
            result = "/".join(parent_ids_from_port_list)
        return result

    def _get_module_index_by_relative_path(self, module_rel_path):
        for index, value in self.relative_address.iteritems():
            if value == module_rel_path:
                return index
