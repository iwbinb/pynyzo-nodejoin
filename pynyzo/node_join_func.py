import argparse
from time import time

from pynyzo import config
from pynyzo.connection import Connection
from pynyzo.helpers import tornado_logger
from pynyzo.message import Message
from pynyzo.messages.nodejoin import NodeJoin
from pynyzo.messagetype import MessageType

def propagate(target_ip, username, socks_host, socks_port, private_key):

    verbose = True
    target_port = 9444

    app_log = tornado_logger()

    config.load()
    connection_args_dict = dict(verbose=verbose)
    message_args_dict = dict(app_log=app_log)

    message_args_dict['sourceNodePrivateKey'] = private_key

    if (socks_host is None and socks_port is not None) or (
        socks_host is not None and socks_port is None):
        raise Exception('Socks port or socks host is not provided')

    if socks_host is not None:
        connection_args_dict.update({
            'socks_host': socks_host,
            'socks_port': socks_port
        })

    connection = Connection(target_ip, **connection_args_dict)

    request = NodeJoin(target_port, username, app_log=app_log)
    message = Message(MessageType.NodeJoin3, request, **message_args_dict)
    res = connection.fetch(message)
    print(res.to_json())
