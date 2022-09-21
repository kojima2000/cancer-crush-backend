# ================================================== #
#              COMMAND LINE INTERFACE                #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 09/20/2022                                #
# Last Edited: 09/20/2022                            #
# ================================================== #
#                                                    #
# ================================================== #

import click
from . import __version__
from .server.server import start_server
from .config.configLoader import ConfigLoader

@click.command()
@click.version_option(version=__version__)
@click.option('--socket', type=str, help="Serves API through specified UNIX "
                                         "domain socket.")
@click.option('--port', type=int, default=8080, help="Sets a port for API to "
                                                     "run on.")
def main(socket, port):
    """
    Command line interface for Cancer Crush backend API
    :param socket: specifies a UNIX socket to serve API on
    :param port: specifies port to serve API on
    """
    print('Server running on localhost:{port}...'.format(port=port))
    start_server(socket, port)

# ================================================== #
#                        EOF                         #
# ================================================== #
