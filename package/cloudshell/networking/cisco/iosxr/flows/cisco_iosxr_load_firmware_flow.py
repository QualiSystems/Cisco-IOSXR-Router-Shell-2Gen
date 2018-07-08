#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
from collections import OrderedDict

from cloudshell.devices.networking_utils import UrlParser
from cloudshell.networking.cisco.flows.cisco_load_firmware_flow import CiscoLoadFirmwareFlow
from cloudshell.networking.cisco.iosxr.command_actions.cisco_iosxr_system_actions import CiscoIOSXRAdminSystemActions


class CiscoIOSXRLoadFirmwareFlow(CiscoLoadFirmwareFlow):
    def __init__(self, cli_handler, logger, packages_to_install):
        super(CiscoIOSXRLoadFirmwareFlow, self).__init__(cli_handler, logger)
        self._packages_to_add = packages_to_install
        if self._packages_to_add == "*" or self._packages_to_add.lower() == "all":
            self._packages_to_add = ""

    def execute_flow(self, path, vrf, timeout):
        """Load a firmware onto the device

        :param path: The path to the firmware file, including the firmware file name
        :param vrf: Virtual Routing and Forwarding Name
        :param timeout:
        :return:
        """

        full_path_dict = UrlParser().parse_url(path)
        firmware_file_name = full_path_dict.get(UrlParser.FILENAME)
        file_extension = None
        success = False
        result_dict = {}
        _pkgs_to_add = []
        remote_path = path.replace("{}".format(firmware_file_name), "").rstrip("/")
        with self._cli_handler.get_cli_service(self._cli_handler.admin_mode) as admin_session:
            admin_actions = CiscoIOSXRAdminSystemActions(admin_session, self._logger)

            try:
                admin_actions.show_install_repository()
            except Exception as e:
                if vrf and vrf not in remote_path:
                    remote_path = remote_path.replace("{}".format(full_path_dict.get(UrlParser.HOSTNAME)),
                                                      "{};{}".format(full_path_dict.get(UrlParser.HOSTNAME), vrf))
                file_extension_match = re.search("\.[a-z]{3}$", firmware_file_name, re.IGNORECASE)
                if file_extension_match:
                    file_extension = file_extension_match.group().lstrip(".")

            if self._packages_to_add:
                _pkgs_to_add = self._packages_to_add.lower().split(" ")

            output = admin_actions.install_add_source(path=remote_path, file_extension=file_extension,
                                                      file_name=firmware_file_name)
            if "no new packages available to be activated" in output.lower():
                raise Exception("Failed to load firmware: no new packages available to be installed (activated)")
            pkgs_for_install, pkgs_to_skip = self._analyze_packages(output, _pkgs_to_add)
            for pkg in pkgs_to_skip:
                package_name = re.sub("^.*:", "", pkg)
                if _pkgs_to_add and package_name.lower() not in _pkgs_to_add:
                    continue
                result_dict[package_name] = "Package is already installed, skipping."
            if not pkgs_for_install:
                self._logger.info(self._prepare_output(result_dict))
                raise Exception("Failed to load firmware: No new packages available to be installed (activated).")

            admin_actions.install_activate(pkgs_for_install)
            admin_actions.install_commit()
            active_pkgs = admin_actions.show_install_active()
            for pkg in pkgs_for_install:
                package_name = re.sub("^.*:", "", pkg)
                if package_name not in active_pkgs:
                    result_dict[package_name] = "Failed to install package, please see logs for details."
                else:
                    success = True
                    result_dict[package_name] = "Successfully installed!"
            if not success:
                raise Exception("Failed to load firmware. Please check logs for details.")
        return self._prepare_output(result_dict)

    def _prepare_output(self, result_dict):
        return "\n".join(["{}: {}".format(key, value) for key, value in result_dict.iteritems()])

    def _analyze_packages(self, output, packages):
        _pkgs_to_add = []
        _pkgs_to_skip = []
        available_pkgs_re_iter = re.finditer("(?P<type>Info|warning): *(?P<message>\S+\d+(.\d+)+)$", output,
                                             re.MULTILINE + re.IGNORECASE) or []
        for item in available_pkgs_re_iter:
            match_dict = item.groupdict()

            package_name = re.sub("^.*:", "", match_dict.get("message").lower())
            if re.search("\Wpie\W", package_name):
                continue
            if match_dict.get("type").lower() == "warning":
                _pkgs_to_skip.append(match_dict.get("message"))
                continue
            if match_dict.get("type").lower() == "info":
                if not self._packages_to_add or package_name in packages:
                    if match_dict.get("message").lower() not in _pkgs_to_add:
                        _pkgs_to_add.append(match_dict.get("message"))
        return _pkgs_to_add, _pkgs_to_skip
