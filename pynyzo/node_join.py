import argparse
from time import time

from pynyzo import config
from pynyzo.connection import Connection
from pynyzo.helpers import tornado_logger
from pynyzo.message import Message
from pynyzo.messages.nodejoin import NodeJoin
from pynyzo.messagetype import MessageType


def main():
    parser = argparse.ArgumentParser(description='Nyzo node join test')
    parser.add_argument("-I", "--ip", type=str, default='127.0.0.1', help="IP to query (default 127.0.0.1)")
    parser.add_argument("-p", "--port", type=int, default=9444, help='Port to query')
    parser.add_argument("-u", "--user", type=str, help='Username')
    parser.add_argument("-v", "--verbose", action="count", default=True, help='Be verbose.')
    parser.add_argument("-sh", "--socks_host", type=str, help='Socks5 host')
    parser.add_argument("-sp", "--socks_port", type=int, help='Socks5 port')
    parser.add_argument("-i", "--identifier", type=str, help='Source node identifier')
    parser.add_argument("-s", "--signature", type=str, help='Source node signature')
    parser.add_argument("-sip", "--source_ip", type=int, help='Source ip address')
    parser.add_argument("-pkey", "--private_key", type=str, help='Private key string')
    args = parser.parse_args()

    app_log = tornado_logger()

    config.load()
    connection_args_dict = dict(verbose=args.verbose)
    message_args_dict = dict(app_log=app_log)
    if args.identifier is not None:
        if args.signature is None:
            raise Exception('Signature data should be provided as well')
        try:
            print('hi')
            message_args_dict.update({
                'timestamp': int(time() * 1000),
                'sourceNodeIdentifier': args.identifier.encode(),
                'sourceNodeSignature': args.signature.encode()
            })
        except Exception:
            raise Exception("Provided data in the arguments for identifier or signature are not correct")

    message_args_dict['sourceNodePrivateKey'] = args.private_key

    if (args.socks_host is None and args.socks_port is not None) or (
        args.socks_host is not None and args.socks_port is None):
        raise Exception('Socks port or socks host is not provided')

    if args.socks_host is not None:
        connection_args_dict.update({
            'socks_host': args.socks_host,
            'socks_port': args.socks_port
        })
    connection = Connection(args.ip, **connection_args_dict)

    request = NodeJoin(args.port, args.user, app_log=app_log)
    message = Message(MessageType.NodeJoin3, request, **message_args_dict)
    res = connection.fetch(message)
    print(res.to_json())


if __name__ == "__main__":
    main()
