#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.cli.command_mode_helper import CommandModeHelper
from cloudshell.networking.cisco.cli.cisco_cli_handler import CiscoCliHandler
from cloudshell.networking.cisco.cli.cisco_command_modes import EnableCommandMode, ConfigCommandMode


class CiscoIOSXRCliHandler(CiscoCliHandler):
    def __init__(self, cli, resource_config, logger, api):
        super(CiscoIOSXRCliHandler, self).__init__(cli, resource_config, logger, api)

    def on_session_start(self, session, logger):
        """Send default commands to configure/clear session outputs
        :return:
        """

        self._enter_enable_mode(session=session, logger=logger)
        session.hardware_expect("terminal length 0", EnableCommandMode.PROMPT, logger)
        session.hardware_expect("terminal width 300", EnableCommandMode.PROMPT, logger)
        self._enter_config_mode(session, logger)
        session.hardware_expect("no logging console", ConfigCommandMode.PROMPT, logger)
        session.hardware_expect("commit", ConfigCommandMode.PROMPT, logger)
        session.hardware_expect("exit", EnableCommandMode.PROMPT, logger)
