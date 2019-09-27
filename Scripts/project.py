import os
import sys
import time
import argparse
import errno
import requests
import json
from halo import Halo

spinner = Halo(text='Loading', spinner='dots')
# Action handlers


def handle_error(err):
    """ Handle errors during project init action. """
    if err.errno == errno.EEXIST:
        spinner.fail('Another file with the same name already exists')
    else:
        spinner.fail('Error trying to create project')


def init_handler(args):
    """ Handle init action. """
    name = args.name
    root = args.dir
    full_path = os.path.join(root, name)

    spinner.start('Creating project structure')
    try:
        os.makedirs(full_path)
    except OSError as err:
        handle_error(err)
        sys.exit(1)

    # Creates client subfolder structure
    if not args.server_only:
        try:
            client_dir = os.path.join(full_path, 'client')
            os.makedirs(client_dir)
        except OSError as err:
            handle_error(err)
            os.rmdir(full_path)
            sys.exit(1)

    # Creates server subfolder structure
    # TODO: Remove `clients` directory if necessary
    if not args.client_only:
        try:
            server_dir = os.path.join(full_path, 'server')
            os.makedirs(server_dir)
        except OSError as err:
            handle_error(err)
            os.rmdir(full_path)
            sys.exit()


    # Save project config into an object
    # We will save this object to file after
    project_config = {
        'name': name,
        'version': '0.0.1',
        'server': {
            'exists': not args.client_only
        },
        'client': {
            'exists': not args.server_only
        }
    }

    # Write configs to file
    filename = os.path.join(full_path, 'project_config.json')
    with open(filename, 'w') as f:
        json.dump(project_config, f, indent=2)
    spinner.succeed('Finished to create project structure')


def ignore_handler(args):
    """ Handle ignore action. """
    res = requests.get('https://gitignore.io/api/list')
    predefined = []

    for line in res.text.splitlines():
        words = line.split(',')
        predefined += words

    availables = []
    not_availables = []
    for t in args.target:
        if t not in predefined:
            not_availables.append(t)
        else:
            availables.append(t)

    io = requests.get('https://gitignore.io/api/%s' % ','.join(availables))
    print(io.text)


# Argument parser
parser = argparse.ArgumentParser(
    prog='project', description='CLI to manage projects')

parser.add_argument('--version', '-v', action='version',
                    version='%(prog)s 0.1')

# Add subparsers for each available action
subparsers = parser.add_subparsers(help='available subcommands')

# Parser for action `init`
parser_action_init = subparsers.add_parser(
    'init',
    help='creates a new project'
)
parser_action_init.add_argument(
    'name',
    metavar='<name>',
    help='project\'s name'
)
parser_action_init.add_argument(
    '--dir', '-d',
    help='project\'s root folder (default is .)',
    default=os.getcwd()
)
parser_action_init.add_argument(
    '--server-only',
    default=False,
    action='store_true',
    help='creates only the server side of this project'
)
parser_action_init.add_argument(
    '--client-only',
    default=False,
    action='store_true',
    help='creates only the client side of this project'
)
parser_action_init.set_defaults(handler=init_handler)

# Parser for action ignore
parser_action_ignore = subparsers.add_parser(
    'ignore',
    help='add content to .gitignore'
)
parser_action_ignore.add_argument(
    'target',
    nargs='+',
    help='list of what should be ignored'
)
parser_action_ignore.set_defaults(handler=ignore_handler)

if __name__ == "__main__":
    args = parser.parse_args()
    if 'handler' in args:
        args.handler(args)
