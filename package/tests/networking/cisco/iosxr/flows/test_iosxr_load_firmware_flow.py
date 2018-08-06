from unittest import TestCase
from mock import MagicMock, patch

from cloudshell.networking.cisco.iosxr.flows.cisco_iosxr_load_firmware_flow import CiscoIOSXRLoadFirmwareFlow


class TestCiscoIOSXRLoadFirmwareFlow(TestCase):

    @patch("cloudshell.networking.cisco.iosxr.flows.cisco_iosxr_load_firmware_flow.CiscoIOSXRAdminSystemActions")
    @patch(
        "cloudshell.networking.cisco.iosxr.flows.cisco_iosxr_load_firmware_flow.CiscoIOSXRLoadFirmwareFlow._get_operation_id",
        return_value=1)
    @patch(
        "cloudshell.networking.cisco.iosxr.flows.cisco_iosxr_load_firmware_flow.CiscoIOSXRLoadFirmwareFlow._filter_packages_for_install",
        return_value=["package"])
    @patch(
        "cloudshell.networking.cisco.iosxr.flows.cisco_iosxr_load_firmware_flow.CiscoIOSXRLoadFirmwareFlow._install_add_source")
    def test_execute_flow(self, add_src_mock, filter_mock, get_id_mock, sys_actions_mock):
        # Setup
        password = "pass"
        remote_path_template = "ftp://user{}@host{}"
        firmware_file_name = "filename.bin"
        file_path = remote_path_template.format(":{}".format(password), "/{}".format(firmware_file_name))
        vrf = "MGMT"
        assert_remote_path = remote_path_template.format("", ";{}".format(vrf)).replace

        # Act
        firmware_flow = CiscoIOSXRLoadFirmwareFlow(MagicMock(), MagicMock(), "package")
        install_activate_mock = MagicMock(return_value="good")
        sys_actions_mock.return_value.install_activate = install_activate_mock
        sys_actions_mock.return_value.show_install_active.return_value = "package"
        firmware_flow.execute_flow(file_path, vrf, "")

        # Assert
        sys_actions_mock.show_install_repository.called_once_with()
        add_src_mock.called_once_with(admin_actions=sys_actions_mock, remote_path=assert_remote_path,
                                      firmware_file_name=firmware_file_name, password=password)
        install_activate_mock.assert_called_once_with(["package"], admin=firmware_flow._cmd_admin_prefix)
        self.assertFalse(firmware_flow._is_old_iosxr)

    @patch("cloudshell.networking.cisco.iosxr.flows.cisco_iosxr_load_firmware_flow.CiscoIOSXRAdminSystemActions")
    @patch(
        "cloudshell.networking.cisco.iosxr.flows.cisco_iosxr_load_firmware_flow.CiscoIOSXRLoadFirmwareFlow._get_operation_id",
        return_value=1)
    @patch(
        "cloudshell.networking.cisco.iosxr.flows.cisco_iosxr_load_firmware_flow.CiscoIOSXRLoadFirmwareFlow._filter_packages_for_install",
        return_value=["package"])
    @patch(
        "cloudshell.networking.cisco.iosxr.flows.cisco_iosxr_load_firmware_flow.CiscoIOSXRLoadFirmwareFlow._install_add_source")
    def test_execute_flow(self, add_src_mock, filter_mock, get_id_mock, sys_actions_mock):
        # Setup
        password = "pass"
        remote_path_template = "ftp://user{}@host{}"
        firmware_file_name = "filename.bin"
        file_path = remote_path_template.format(":{}".format(password), "/{}".format(firmware_file_name))
        vrf = "MGMT"
        assert_remote_path = remote_path_template.format(":{}".format(password), ";{}".format(vrf)).replace

        # Act
        firmware_flow = CiscoIOSXRLoadFirmwareFlow(MagicMock(), MagicMock(), "")
        install_activate_mock = MagicMock(return_value="good")
        sys_actions_mock.return_value.show_install_repository.side_effect = Exception()
        sys_actions_mock.return_value.install_activate = install_activate_mock
        sys_actions_mock.return_value.show_install_active.return_value = "package"
        firmware_flow.execute_flow(file_path, vrf, "")

        # Assert
        sys_actions_mock.show_install_repository.called_once_with()
        add_src_mock.called_once_with(admin_actions=sys_actions_mock, remote_path=assert_remote_path,
                                      firmware_file_name=firmware_file_name, password=password)
        install_activate_mock.assert_called_once_with(["package"], admin=firmware_flow._cmd_admin_prefix)
        self.assertTrue(firmware_flow._is_old_iosxr)

    def test_operation_id(self):
        # Setup
        id = "73"
        output = "The install operation {} is 4% complete".format(id)
        firmware_flow = CiscoIOSXRLoadFirmwareFlow(MagicMock(), MagicMock(), "")

        # Act
        operation_id = firmware_flow._get_operation_id(output)

        # Assert
        self.assertEqual(id, operation_id)

    @patch("cloudshell.networking.cisco.iosxr.flows.cisco_iosxr_load_firmware_flow.CiscoIOSXRAdminSystemActions")
    @patch(
        "cloudshell.networking.cisco.iosxr.flows.cisco_iosxr_load_firmware_flow.CiscoIOSXRLoadFirmwareFlow._get_operation_id",
        return_value=1)
    def test_install_add_source(self, operation_id_mock, sys_actions_mock):
        # Setup
        remote_path = "remote_path"
        password = "password"
        firmware_file_name = "file_name"
        error_map = {
            "{}/{}\S*\s*could not be found".format(remote_path, firmware_file_name): "{} file not found".format(
                firmware_file_name)}
        action_map = {"[Pp]assword:": lambda session, logger: session.send_line(password, logger)}
        firmware_flow = CiscoIOSXRLoadFirmwareFlow(MagicMock(), MagicMock(), "")

        # Act
        firmware_flow._install_add_source(admin_actions=sys_actions_mock, remote_path=remote_path,
                                          firmware_file_name=firmware_file_name, password=password)

        # Assert
        sys_actions_mock.install_add_source.called_once_with(path=remote_path, file_name=firmware_file_name,
                                                             action_map=action_map, error_map=error_map)
        sys_actions_mock.show_install_request.called_once_with(operation_id=1)

    @patch("cloudshell.networking.cisco.iosxr.flows.cisco_iosxr_load_firmware_flow.CiscoIOSXRAdminSystemActions")
    def test_install_add_source_old_iosxr(self, sys_actions_mock):
        # Setup
        remote_path = "remote_path"
        password = "password"
        file_extension = "tar"
        firmware_file_name = "file_name.tar"
        error_map = {
            "{}/{}\S*\s*could not be found".format(remote_path, firmware_file_name): "{} file not found".format(
                firmware_file_name)}
        action_map = {"[Pp]assword:": lambda session, logger: session.send_line(password, logger)}
        firmware_flow = CiscoIOSXRLoadFirmwareFlow(MagicMock(), MagicMock(), "")
        firmware_flow._is_old_iosxr = True

        # Act
        firmware_flow._install_add_source(admin_actions=sys_actions_mock, remote_path=remote_path,
                                          firmware_file_name=firmware_file_name, password=password)

        # Assert
        sys_actions_mock.install_add_source.called_once_with(path=remote_path, file_extension=file_extension,
                                                             file_name=firmware_file_name,
                                                             admin=firmware_flow._cmd_admin_prefix,
                                                             sync=firmware_flow._sync, action_map=action_map,
                                                             error_map=error_map, )

    @patch("cloudshell.networking.cisco.iosxr.flows.cisco_iosxr_load_firmware_flow.CiscoIOSXRAdminSystemActions")
    @patch(
        "cloudshell.networking.cisco.iosxr.flows.cisco_iosxr_load_firmware_flow.CiscoIOSXRLoadFirmwareFlow._get_packages_for_install",
        return_value=1)
    @patch(
        "cloudshell.networking.cisco.iosxr.flows.cisco_iosxr_load_firmware_flow.CiscoIOSXRLoadFirmwareFlow._get_operation_id",
        return_value=1)
    def test_filter_packages_for_install(self, operation_id_mock, get_pkgs_mock, sys_actions_mock):
        # Setup
        output = "The install operation 1 is 4% complete"
        pkg = "ncs5500-mgbl-3.0.0.0-r6225"
        firmware_flow = CiscoIOSXRLoadFirmwareFlow(MagicMock(), MagicMock(), "")
        sh_install_log_mock = MagicMock(return_value=pkg)
        sys_actions_mock.retrieve_install_log = sh_install_log_mock
        get_pkgs_mock.return_value = [pkg]

        # Act
        result = firmware_flow._filter_packages_for_install(sys_actions_mock, output)

        # Assert
        self.assertEqual([pkg], result)
        get_pkgs_mock.assert_called_once_with([pkg])
        sh_install_log_mock.assert_called_once_with(1)

    @patch("cloudshell.networking.cisco.iosxr.flows.cisco_iosxr_load_firmware_flow.CiscoIOSXRAdminSystemActions")
    @patch(
        "cloudshell.networking.cisco.iosxr.flows.cisco_iosxr_load_firmware_flow.CiscoIOSXRLoadFirmwareFlow._get_packages_for_install",
        return_value=1)
    @patch(
        "cloudshell.networking.cisco.iosxr.flows.cisco_iosxr_load_firmware_flow.CiscoIOSXRLoadFirmwareFlow._get_operation_id",
        return_value=1)
    def test_filter_packages_for_install_no_pkg(self, operation_id_mock, get_pkgs_mock, sys_actions_mock):
        # Setup
        output = "The install operation 1 is 4% complete"
        pkg = """ncs5500-mgbl-3.0.0.0-r6225
ncs5500-mpls-3.0.0.0-r6225
ncs5500-k9-3.0.0.0-r6225
ncs5500-auto-3.0.0.0-r6225
ncs5500-dddd-3.0.0.0-r6225"""
        firmware_flow = CiscoIOSXRLoadFirmwareFlow(MagicMock(), MagicMock(), "")
        sh_install_log_mock = MagicMock(return_value=pkg)
        sys_actions_mock.retrieve_install_log = sh_install_log_mock
        get_pkgs_mock.return_value = pkg.split("\n")

        # Act
        result = firmware_flow._filter_packages_for_install(sys_actions_mock, output)

        # Assert
        self.assertEqual(pkg.split("\n"), result)
        get_pkgs_mock.assert_called_once_with(pkg.split("\n"))
        sh_install_log_mock.assert_called_once_with(1)


    @patch("cloudshell.networking.cisco.iosxr.flows.cisco_iosxr_load_firmware_flow.CiscoIOSXRAdminSystemActions")
    @patch(
        "cloudshell.networking.cisco.iosxr.flows.cisco_iosxr_load_firmware_flow.CiscoIOSXRLoadFirmwareFlow._get_packages_for_install",
        return_value=1)
    @patch(
        "cloudshell.networking.cisco.iosxr.flows.cisco_iosxr_load_firmware_flow.CiscoIOSXRLoadFirmwareFlow._get_operation_id",
        return_value=1)
    def test_filter_packages_for_install_pkg_installed(self, operation_id_mock, get_pkgs_mock, sys_actions_mock):
        # Setup
        output = "The install operation 1 is 4% complete"
        pkg = "ncs5500-mpls-3.0.0.0-r6225"
        pkg_output = """ncs5500-mgbl-3.0.0.0-r6225
ncs5500-mpls-3.0.0.0-r6225
ncs5500-k9-3.0.0.0-r6225
ncs5500-auto-3.0.0.0-r6225
ncs5500-dddd-3.0.0.0-r6225"""
        firmware_flow = CiscoIOSXRLoadFirmwareFlow(MagicMock(), MagicMock(), "")
        sh_install_log_mock = MagicMock(return_value=pkg_output)
        sys_actions_mock.retrieve_install_log = sh_install_log_mock
        get_pkgs_mock.return_value = pkg_output.split("\n")
        sys_actions_mock.show_install_active.return_value = pkg_output.replace(pkg, "").split("\n")

        # Act
        result = firmware_flow._filter_packages_for_install(sys_actions_mock, output)

        # Assert
        self.assertEqual([pkg], result)
        get_pkgs_mock.assert_called_once_with(pkg_output.split("\n"))
        sh_install_log_mock.assert_called_once_with(1)


    @patch("cloudshell.networking.cisco.iosxr.flows.cisco_iosxr_load_firmware_flow.CiscoIOSXRAdminSystemActions")
    @patch(
        "cloudshell.networking.cisco.iosxr.flows.cisco_iosxr_load_firmware_flow.CiscoIOSXRLoadFirmwareFlow._get_legacy_packages_for_install",
        return_value=1)
    def test_filter_packages_for_install_old_iosxr(self, get_pkgs_mock, sys_actions_mock):
        # Setup
        pkg_output = ["ncs5500-mgbl-3.0.0.0-r6225", "ncs5500-mpls-3.0.0.0-r6225", "ncs5500-dddd-3.0.0.0-r6225"]
        output = "The install operation 1 is 4% complete"
        firmware_flow = CiscoIOSXRLoadFirmwareFlow(MagicMock(), MagicMock(), "")
        firmware_flow._is_old_iosxr =True
        get_pkgs_mock.return_value = pkg_output

        # Act
        result = firmware_flow._filter_packages_for_install(sys_actions_mock, output)

        # Assert
        self.assertEqual(pkg_output, result)
        get_pkgs_mock.assert_called_once_with(output)

    @patch("cloudshell.networking.cisco.iosxr.flows.cisco_iosxr_load_firmware_flow.CiscoIOSXRAdminSystemActions")
    @patch(
        "cloudshell.networking.cisco.iosxr.flows.cisco_iosxr_load_firmware_flow.CiscoIOSXRLoadFirmwareFlow._get_legacy_packages_for_install",
        return_value=1)
    def test_filter_packages_for_install_old_iosxr(self, get_pkgs_mock, sys_actions_mock):
        # Setup
        output = "no new packages available to be activated"
        firmware_flow = CiscoIOSXRLoadFirmwareFlow(MagicMock(), MagicMock(), "")
        firmware_flow._is_old_iosxr =True

        # Act
        try:
            firmware_flow._filter_packages_for_install(sys_actions_mock, output)
        except Exception as e:
            # Assert
            self.assertEqual("Failed to load firmware: no new packages available to be installed (activated)", e.message)

    def test_get_packages_for_install(self):
        # Setup
        pkg_output = ["ncs5500-mgbl-3.0.0.0-r6225", "ncs5500-mpls-3.0.0.0-r6225", "ncs5500-dddd-3.0.0.0-r6225"]
        firmware_flow = CiscoIOSXRLoadFirmwareFlow(MagicMock(), MagicMock(), "")

        # Act
        result = firmware_flow._get_packages_for_install(pkg_output)
        firmware_flow._packages_to_add = ["ncs5500-mgbl-3.0.0.0-r6225"]
        result1 = firmware_flow._get_packages_for_install(pkg_output)
        firmware_flow._packages_to_add = ["ncs5500-mgbl-3.0.0.0-r6225", "ncs5500-mpls-3.0.0.0-r6225", "ncs5500-fff-3.0.0.0-r6225"]
        result2 = firmware_flow._get_packages_for_install(pkg_output)

        # Assert
        self.assertEqual(result, pkg_output)
        self.assertEqual(result1, ["ncs5500-mgbl-3.0.0.0-r6225"])
        self.assertEqual(result2, ["ncs5500-mgbl-3.0.0.0-r6225", "ncs5500-mpls-3.0.0.0-r6225"])
        self.assertIsNotNone(firmware_flow._result_dict.get("ncs5500-fff-3.0.0.0-r6225"))
        self.assertEqual(firmware_flow._result_dict.get("ncs5500-fff-3.0.0.0-r6225"), "Package not found, skipping.")

    def test_get_legacy_packages_for_install(self):
        # Setup
        pkg_output = """and will be added to the entire router:
Info:     
Info:         asr9k-px-5.3.4.CSCvi52005.txt (skipped - not a pie)
Info:         asr9k-px-5.3.4.CSCvi52005.pie
Info:     
The install operation will continue asynchronously.
RP/0/RSP0/CPU0:ipf-zbl1311-r-rr-11#Info:     The following package is now available to be activated:
Info:     
Info:         disk0:asr9k-px-5.3.4.CSCvi52005-1.0.0
Info:     
Info:     The package can be activated across the entire router.
Info:     
Install operation 14 completed successfully at 16:57:32 CEST Tue Jun 19 2018.
 """
        firmware_flow = CiscoIOSXRLoadFirmwareFlow(MagicMock(), MagicMock(), "")

        # Act
        result = firmware_flow._get_legacy_packages_for_install(pkg_output)
        firmware_flow._packages_to_add = ["asr9k-px-5.3.4.CSCvi52005-1.0.0"]
        result1 = firmware_flow._get_legacy_packages_for_install(pkg_output)
        firmware_flow._packages_to_add = ["ncs5500-mgbl-3.0.0.0-r6225", "ncs5500-mpls-3.0.0.0-r6225", "ncs5500-fff-3.0.0.0-r6225"]
        result2 = firmware_flow._get_legacy_packages_for_install(pkg_output)

        # Assert
        self.assertEqual(result, ["disk0:asr9k-px-5.3.4.CSCvi52005-1.0.0"])
        self.assertEqual(result1, ["disk0:asr9k-px-5.3.4.CSCvi52005-1.0.0"])
        self.assertEqual(result2, [])
        # self.assertIsNotNone(firmware_flow._result_dict.get("ncs5500-fff-3.0.0.0-r6225"))
        # self.assertEqual(firmware_flow._result_dict.get("ncs5500-fff-3.0.0.0-r6225"), "Package not found, skipping.")
