import re
from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor
from cloudshell.networking.cisco.command_actions.system_actions import SystemActions
from cloudshell.networking.cisco.iosxr.command_templates.cisco_ios_xr_cmd_templates import COMMIT_REPlACE, LOAD


class CiscoIOSXRSystemActions(SystemActions):
    def __init__(self, cli_service, logger):
        super(CiscoIOSXRSystemActions, self).__init__(cli_service, logger)

    def load(self, source_file, vrf=None, action_map=None, error_map=None):

        if vrf:
            load_result = CommandTemplateExecutor(self._cli_service, LOAD).execute_command(
                source_file=source_file, vrf=vrf, action_map=action_map, error_map=error_map)
        else:
            load_result = CommandTemplateExecutor(self._cli_service, LOAD).execute_command(
                source_file=source_file, action_map=action_map, error_map=error_map)

        return load_result

    def replace_config(self, action_map=None, error_map=None):
        commit_result = CommandTemplateExecutor(self._cli_service, COMMIT_REPlACE).execute_command(
            action_map=action_map, error_map=error_map)
        return commit_result

    @staticmethod
    def validate_replace_config_success(output):
        error_match_commit = re.search(r'(ERROR|[Ee]rror).*\n', output)

        if error_match_commit:
            error_str = error_match_commit.group()
            raise Exception('validate_replace_config_success', 'load error: ' + error_str)

    @staticmethod
    def validate_load_success(output):
        match_success = re.search(r"[\[\(][1-9][0-9]*[\)\]].*bytes", output, re.IGNORECASE | re.MULTILINE)
        if not match_success:
            error_str = "Failed to restore configuration, please check logs"
            match_error = re.search(r" Can't assign requested address|[Ee]rror:.*\n|%.*$",
                                    output, re.IGNORECASE | re.MULTILINE)

            if match_error:
                error_str = 'load error: ' + match_error.group()

            raise Exception('validate_load_success', error_str)
