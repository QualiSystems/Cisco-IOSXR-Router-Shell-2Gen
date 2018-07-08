from collections import OrderedDict
from cloudshell.cli.command_template.command_template import CommandTemplate

COMMIT_REPlACE = CommandTemplate(command="commit replace", action_map=OrderedDict({
    '[\[\(][Nn]o[\)\]]|\[confirm\]': lambda session, logger: session.send_line('yes', logger)}))

LOAD = CommandTemplate(command="load {source_file} [vrf {vrf}]", action_map=OrderedDict({
    '[\[\(][Yy]es/[Nn]o[\)\]]': lambda session, logger: session.send_line('yes', logger),
    '\[confirm\]': lambda session, logger: session.send_line("", logger),
    '\(y\/n\)': lambda session, logger: session.send_line('y', logger),
    '[\[\(][Yy]/[Nn][\)\]]': lambda session, logger: session.send_line('y', logger),
    'overwrit+e': lambda session, logger: session.send_line('yes', logger),
    'Do you wish to proceed': lambda session, logger: session.send_line('yes', logger)
}))

COMMIT = CommandTemplate(command="commit", action_map=OrderedDict({
    '[\[\(][Nn]o[\)\]]': lambda session, logger: session.send_line('yes', logger),
    '\[confirm\]': lambda session, logger: session.send_line('', logger)}),
                         error_map=OrderedDict({"% Failed to commit": "Failed to commit changes"}))

INSTALL_ADD_SRC = CommandTemplate(command="install add source {path} [{file_extension}] {file_name} [vrf {vrf}] synchronous",
                                  error_map=OrderedDict({"operation \d+ failed": "Failed to load firmware"}))

SHOW_INSTALL_REPO = CommandTemplate(command="show install repository",
                                    error_map=OrderedDict([("[Ii]nvalid\s*([Ii]nput|[Cc]ommand)|[Cc]ommand rejected",
                                                            "'show install repository' command is not supported")]))

INSTALL_ACTIVATE = CommandTemplate(command="install activate {feature_names} synchronous",
                                   action_map=OrderedDict({
                                       '[\[\(][Yy]es/[Nn]o[\)\]]': lambda session, logger: session.send_line('yes',
                                                                                                             logger)}),
                                   error_map=OrderedDict({"operation \d+ failed": "Failed to load firmware",
                                                          "Error:.*$": "Failed to load firmware"}))

SHOW_PIE_INFO = CommandTemplate(command="show install pie-info {path}")

INSTALL_COMMIT = CommandTemplate(command="install commit",
                                 action_map=OrderedDict({
                                     '[\[\(][Yy]es/[Nn]o[\)\]]': lambda session, logger: session.send_line('yes',
                                                                                                           logger)}),
                                 error_map=OrderedDict({"operation \d+ failed": "Failed to load firmware"}))

SHOW_INSTALL_ACTIVE = CommandTemplate(command="show install active")

SHOW_INSTALL_COMMIT = CommandTemplate(command="show install commit")
