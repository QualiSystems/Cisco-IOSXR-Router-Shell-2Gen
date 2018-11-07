from unittest import TestCase
from cloudshell.cli.cli_service import CliService
from mock import MagicMock, create_autospec, patch

from cloudshell.networking.cisco.iosxr.command_actions.cisco_iosxr_system_actions import CiscoIOSXRAdminSystemActions


class TestCiscoIOSXRAdminActions(TestCase):

    def setUp(self):
        self._cli_service = MagicMock()
        self._system_admin_actions = CiscoIOSXRAdminSystemActions(cli_service=self._cli_service,
                                                                  logger=MagicMock())

    @patch("cloudshell.networking.cisco.iosxr.command_actions.cisco_iosxr_system_actions.CommandTemplateExecutor")
    @patch("cloudshell.networking.cisco.iosxr.command_actions.cisco_iosxr_system_actions.ios_xr_cmd_templates")
    def test_install_add_source(self, ios_xr_cmd_templates_mock, cte_mock):
        # Setup
        exec_cmd_mock = MagicMock()
        cte_mock.return_value.execute_command = exec_cmd_mock
        file_extension = "tar"
        file_name = "asr9k-px-5.3.4.CSCvi52005.tar"
        path = "ftp://10.10.10.10/ASR9xxx/iosxr-5.3.3/"

        # Act
        self._system_admin_actions.install_add_source(path=path, file_name=file_name, file_extension=file_extension)

        # Assert
        cte_mock.assert_called_once_with(self._cli_service, ios_xr_cmd_templates_mock.INSTALL_ADD_SRC, action_map=None,
                                         error_map=None, timeout=self._system_admin_actions.INSTALL_ADD_SOURCE_TIMEOUT)
        exec_cmd_mock.assert_called_once_with(admin=None, path=path, file_extension=file_extension, file_name=file_name,
                                              sync=None)

    @patch("cloudshell.networking.cisco.iosxr.command_actions.cisco_iosxr_system_actions.CommandTemplateExecutor")
    @patch("cloudshell.networking.cisco.iosxr.command_actions.cisco_iosxr_system_actions.ios_xr_cmd_templates")
    def test_install_activate(self, ios_xr_cmd_templates_mock, cte_mock):
        # Setup
        exec_cmd_mock = MagicMock()
        cte_mock.return_value.execute_command = exec_cmd_mock
        feature_names = ["disk0:asr9k-px-5.3.4"]

        # Act
        self._system_admin_actions.install_activate(feature_names=feature_names)

        # Assert
        cte_mock.assert_called_once_with(self._cli_service, ios_xr_cmd_templates_mock.INSTALL_ACTIVATE, action_map=None,
                                         error_map=None)
        exec_cmd_mock.assert_called_once_with(admin=None, feature_names=" ".join(feature_names))

    @patch("cloudshell.networking.cisco.iosxr.command_actions.cisco_iosxr_system_actions.CommandTemplateExecutor")
    @patch("cloudshell.networking.cisco.iosxr.command_actions.cisco_iosxr_system_actions.ios_xr_cmd_templates")
    def test_install_commit(self, ios_xr_cmd_templates_mock, cte_mock):
        # Setup
        exec_cmd_mock = MagicMock()
        cte_mock.return_value.execute_command = exec_cmd_mock

        # Act
        self._system_admin_actions.INSTALL_COMMIT_TIMEOUT = 0.1
        self._system_admin_actions.install_commit()

        # Assert
        cte_mock.assert_called_once_with(self._cli_service, ios_xr_cmd_templates_mock.INSTALL_COMMIT, action_map=None,
                                         error_map=None)
        exec_cmd_mock.assert_called_once_with(admin=None)

    @patch("cloudshell.networking.cisco.iosxr.command_actions.cisco_iosxr_system_actions.CommandTemplateExecutor")
    def test_show_install_request(self, cte_mock):
        # Setup
        exec_cmd_mock = MagicMock(
            side_effect=["The install operation 73 is 4% complete", "The install operation 73 is 4% complete",
                         "The install operation 73 is 4% complete", "The install operation 73 is 4% complete",
                         "The install operation 73 is 4% complete", "No install operation in progress"])
        cte_mock.return_value.execute_command = exec_cmd_mock

        # Act
        self._system_admin_actions.SHOW_REQUEST_TIMEOUT = 0.1
        result = self._system_admin_actions.show_install_request(10)

        # Assert
        self.assertTrue(result)
        self.assertTrue(cte_mock.called)
        self.assertEqual(exec_cmd_mock.call_count, 6)

    @patch("cloudshell.networking.cisco.iosxr.command_actions.cisco_iosxr_system_actions.CommandTemplateExecutor")
    def test_show_install_request_false(self, cte_mock):
        output = ["The install operation 73 is 4% complete"] * 20
        output.extend(["failed to read buffer"] * 10)
        # Setup
        exec_cmd_mock = MagicMock(
            side_effect=output)
        cte_mock.return_value.execute_command = exec_cmd_mock

        # Act
        self._system_admin_actions.SHOW_REQUEST_TIMEOUT = 0.1
        result = self._system_admin_actions.show_install_request(73)

        # Assert
        self.assertFalse(result)
        self.assertTrue(cte_mock.called)
        self.assertEqual(30, exec_cmd_mock.call_count)

    @patch("cloudshell.networking.cisco.iosxr.command_actions.cisco_iosxr_system_actions.CommandTemplateExecutor")
    def test_show_install_request_true(self, cte_mock):
        output = ["The install operation 73 is 4% complete"] * 9
        output.append("No install operation in progress")
        # Setup
        exec_cmd_mock = MagicMock(
            side_effect=output)
        cte_mock.return_value.execute_command = exec_cmd_mock

        # Act
        self._system_admin_actions.SHOW_REQUEST_TIMEOUT = 0.1
        result = self._system_admin_actions.show_install_request(73)

        # Assert
        self.assertTrue(result)
        self.assertTrue(cte_mock.called)
        self.assertEqual(10, exec_cmd_mock.call_count)