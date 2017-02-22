from collections import OrderedDict
from cloudshell.cli.command_template.command_template import CommandTemplate

COMMIT_REPlACE = CommandTemplate(command="commit replace", action_map=OrderedDict({
    '[\[\(][Nn]o[\)\]]|\[confirm\]': lambda session, logger: session.send_line('yes', logger)}))

LOAD = CommandTemplate(command="load {source_file} [vrf {vrf}]", action_map=OrderedDict({
    '[\[\(][Yy]es/[Nn]o[\)\]]|\[confirm\]': lambda session, logger: session.send_line('yes', logger),
    '\(y\/n\)': lambda session, logger: session.send_line('y', logger),
    '[\[\(][Yy]/[Nn][\)\]]': lambda session, logger: session.send_line('y', logger),
    'overwrit+e': lambda session, logger: session.send_line('yes', logger),
    'Do you wish to proceed': lambda session, logger: session.send_line('yes', logger)
}))
