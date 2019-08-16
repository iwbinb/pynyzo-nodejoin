import argparse
from time import time

from pynyzo import config
from pynyzo.connection import Connection
from pynyzo.helpers import tornado_logger
from pynyzo.message import Message
from pynyzo.messages.nodejoin import NodeJoin
from pynyzo.messagetype import MessageType

def get_new_private():
    with open('data/test2.txt', 'r') as f:
        pk_list = f.readlines()

    new_pk = pk_list[0]
    pk_list.pop(0)

    w_str = str()
    for i in pk_list:
        w_str = w_str + i

    with open('data/test2.txt', 'w') as f:
        f.write(w_str)

    return new_pk.strip()

def update_ip_data(ip, k, v):
    data_dict = load_from_data(None)
    ip_inner = data_dict[ip]
    ip_inner.update({k: v})
    data_dict.update({ip: ip_inner})
    with open('data/assign', 'w') as f:
        f.write(str(data_dict))

def assign_to_ip(ip):
    import random
    r = random.randint(1, 99999999999999)
    u = 'h' + str(r)
    data_dict = load_from_data(None)
    inner_dict = {'private_key': get_new_private(), 'name': u, 'last_ts': None}
    data_dict.update({ip: inner_dict})
    with open('data/assign', 'w') as f:
        f.write(str(data_dict))

    return inner_dict


def load_from_data(s_ip):
    import ast
    data = open('data/assigns', 'r').read()
    data_dict = ast.literal_eval(data)
    if s_ip is not None:
        for ip, inner_dict in data_dict.items():
            if s_ip == ip:
                return inner_dict
        return None
    else:
        return data_dict


def propagate(target_ip, socks_host, socks_port):

    private_key = None
    username = None

    rres = load_from_data(socks_host)
    if rres is None:
        res = assign_to_ip(socks_host)
        username = res['name']
        private_key = res['private_key']
    else:
        username = rres['name']
        private_key = rres['private_key']

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


propagate('verifier4.nyzo.co', '41.66.82.21', 9999)
