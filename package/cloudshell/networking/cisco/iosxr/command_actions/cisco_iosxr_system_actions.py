import re
from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor
from cloudshell.cli.session.session_exceptions import SessionException
from cloudshell.networking.cisco.command_actions.system_actions import SystemActions
import cloudshell.networking.cisco.iosxr.command_templates.cisco_ios_xr_cmd_templates as ios_xr_cmd_templates


class CiscoIOSXRSystemActions(SystemActions):
    def __init__(self, cli_service, logger):
        super(CiscoIOSXRSystemActions, self).__init__(cli_service, logger)

    def load(self, source_file, vrf=None, action_map=None, error_map=None):
        load_cmd = CommandTemplateExecutor(self._cli_service, ios_xr_cmd_templates.LOAD, action_map=action_map,
                                           error_map=error_map)
        if vrf:
            load_result = load_cmd.execute_command(source_file=source_file, vrf=vrf)
        else:
            load_result = load_cmd.execute_command(source_file=source_file)

        match_success = re.search(r"[\[\(][1-9][0-9]*[\)\]].*bytes|^([1-9][0-9]*)+\s*bytes\s*(parsed|process+ed)",
                                  load_result, re.IGNORECASE | re.MULTILINE)
        if not match_success:
            error_str = "Failed to restore configuration, please check logs"
            match_error = re.search(r" Can't assign requested address|[Ee]rror:.*\n|%.*$",
                                    load_result, re.IGNORECASE | re.MULTILINE)

            if match_error:
                error_str = 'load error: ' + match_error.group()

            raise Exception('validate_load_success', error_str)

        return load_result

    def replace_config(self, action_map=None, error_map=None):
        commit_result = CommandTemplateExecutor(self._cli_service, ios_xr_cmd_templates.COMMIT_REPlACE,
                                                action_map=action_map,
                                                error_map=error_map).execute_command()

        error_match_commit = re.search(r'(ERROR|[Ee]rror).*\n', commit_result)

        if error_match_commit:
            error_str = error_match_commit.group()
            raise Exception('validate_replace_config_success', 'load error: ' + error_str)
        return commit_result

    def commit(self, action_map=None, error_map=None):
        CommandTemplateExecutor(self._cli_service, ios_xr_cmd_templates.COMMIT, action_map=action_map,
                                error_map=error_map).execute_command()


class CiscoIOSXRAdminSystemActions(object):
    def __init__(self, cli_service, logger):
        self._cli_service = cli_service
        self._logger = logger

    def get_available_remote_packages(self, available_pkgs, is_old_iosxr=False):
        return []

    def install_add_source(self, path, file_name, file_extension, vrf=None, action_map=None, error_map=None):
        return CommandTemplateExecutor(self._cli_service, ios_xr_cmd_templates.INSTALL_ADD_SRC, action_map=action_map,
                                       error_map=error_map, timeout=600).execute_command(path=path,
                                                                                         file_extension=file_extension,
                                                                                         file_name=file_name, vrf=vrf)

    def install_activate(self, feature_names, action_map=None, error_map=None):
        return CommandTemplateExecutor(self._cli_service, ios_xr_cmd_templates.INSTALL_ACTIVATE, action_map=action_map,
                                       error_map=error_map).execute_command(feature_names=" ".join(feature_names))

    def show_install_repository(self, action_map=None, error_map=None):
        return CommandTemplateExecutor(self._cli_service, ios_xr_cmd_templates.SHOW_INSTALL_REPO, action_map=action_map,
                                       error_map=error_map).execute_command()

    def install_commit(self, action_map=None, error_map=None):
        return CommandTemplateExecutor(self._cli_service, ios_xr_cmd_templates.INSTALL_COMMIT, action_map=action_map,
                                       error_map=error_map).execute_command()

    def show_install_active(self, action_map=None, error_map=None):
        return CommandTemplateExecutor(self._cli_service, ios_xr_cmd_templates.SHOW_INSTALL_ACTIVE,
                                       action_map=action_map,
                                       error_map=error_map).execute_command()

    def show_install_commit(self, action_map=None, error_map=None):
        return CommandTemplateExecutor(self._cli_service, ios_xr_cmd_templates.SHOW_INSTALL_COMMIT,
                                       action_map=action_map,
                                       error_map=error_map).execute_command()

    def show_install_pie_info(self, path, action_map=None, error_map=None):
        return CommandTemplateExecutor(self._cli_service, ios_xr_cmd_templates.SHOW_PIE_INFO,
                                       action_map=action_map,
                                       error_map=error_map).execute_command(path=path)

