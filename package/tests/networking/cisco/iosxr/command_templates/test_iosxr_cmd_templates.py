from unittest import TestCase

from cloudshell.networking.cisco.iosxr.command_templates import cisco_ios_xr_cmd_templates


class TestCiscoIOSXRCmdTemplates(TestCase):

    def setUp(self):
        self.path = "ftp://admin:password@10.10.10.10/CloudShell/config"
        self.firmware_file_name = "name"

    def test_install_commit(self):
        output = "install commit"
        output_admin = "admin install commit"
        commit = cisco_ios_xr_cmd_templates.INSTALL_COMMIT.get_command(admin=None)
        commit_admin = cisco_ios_xr_cmd_templates.INSTALL_COMMIT.get_command(admin="")

        self.assertEqual(output, commit.get('command'))
        self.assertEqual(output_admin, commit_admin.get('command'))

    def test_install_activate(self):
        packages_new = "pkg1 pkg2"
        packages_old = "disk0:pkg1 disk0:pkg2"
        output = "install activate {}".format(packages_new)
        output_admin = "admin install activate {} synchronous".format(packages_old)
        activate = cisco_ios_xr_cmd_templates.INSTALL_ACTIVATE.get_command(admin=None, feature_names=packages_new,
                                                                           sync=None)
        activate_admin = cisco_ios_xr_cmd_templates.INSTALL_ACTIVATE.get_command(admin="", feature_names=packages_old,
                                                                                 sync="")

        self.assertEqual(output, activate.get('command'))
        self.assertEqual(output_admin, activate_admin.get('command'))

    def test_install_add_source(self):
        file_extension = "tar"
        result1 = "install add source {} {}".format(self.path, self.firmware_file_name)
        result2 = "admin install add source {} {} synchronous".format(self.path, self.firmware_file_name)
        result3 = "admin install add source {} {} {} synchronous".format(self.path, file_extension,
                                                                         self.firmware_file_name)
        install_add_source_1 = cisco_ios_xr_cmd_templates.INSTALL_ADD_SRC.get_command(path=self.path,
                                                                                      file_extension=None,
                                                                                      file_name=self.firmware_file_name,
                                                                                      admin=None,
                                                                                      sync=None)
        install_add_source_2 = cisco_ios_xr_cmd_templates.INSTALL_ADD_SRC.get_command(path=self.path,
                                                                                      file_extension=None,
                                                                                      file_name=self.firmware_file_name,
                                                                                      admin="",
                                                                                      sync="")
        install_add_source_3 = cisco_ios_xr_cmd_templates.INSTALL_ADD_SRC.get_command(path=self.path,
                                                                                      file_extension=file_extension,
                                                                                      file_name=self.firmware_file_name,
                                                                                      admin="",
                                                                                      sync="")

        self.assertEqual(result1, install_add_source_1.get('command'))
        self.assertEqual(result2, install_add_source_2.get('command'))
        self.assertEqual(result3, install_add_source_3.get('command'))
