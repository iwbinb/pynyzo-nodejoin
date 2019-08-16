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

def ips_list():
    import requests
    # res = requests.get('http://95.216.184.40/nodes.txt')
    res = requests.get('http://94.130.179.46/nyzo.html')
    res = res.content.decode('utf-8')
    res = res.split('<tr>')
    ip_list = ['95.216.184.40', '94.130.179.46', 'verifier0.nyzo.co', 'verifier1.nyzo.co', 'verifier2.nyzo.co', 'verifier3.nyzo.co', 'verifier4.nyzo.co', 'verifier5.nyzo.co', 'verifier6.nyzo.co', 'verifier7.nyzo.co', 'verifier8.nyzo.co', 'verifier9.nyzo.co']
    for i in res:
        r = i.split('</td>')
        try:
            if 'in' in r[6].lower():
                ip = r[0].split('>')
                ip = ip[len(ip)-1]
                print(ip)
                ip_list.append(ip)
                print(len(ip_list))
        except:
            pass
        # propagata nodejoin to all the nodes in the mesh, if other queue nodes join we wish for them
        # to also have a record of the IP/PK/UN
        # ip = r[0].split('>')
        # ip = ip[len(ip)-1]
        # ip_list.append(ip)

    print('About to propagate to {} nodes in the mesh'.format(len(ip_list)))
    return ip_list


def load_from_data(s_ip):
    import ast
    data = open('data/assign', 'r').read()
    data_dict = ast.literal_eval(data)
    if s_ip is not None:
        for ip, inner_dict in data_dict.items():
            if s_ip == ip:
                return inner_dict
        return None
    else:
        return data_dict


def propagate(socks_host, socks_port):
    import subprocess
    from threading import Thread, Event
    stop_it = Event()
    ips = ips_list()

    def call(target_ip):
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

        # print(private_key)

        verbose = True
        target_port = 9444

        app_log = tornado_logger()

        config.load()
        connection_args_dict = dict(verbose=verbose)
        message_args_dict = dict(app_log=app_log)

        message_args_dict.update({
            'timestamp': int(time() * 1000)
            # 'sourceNodePrivateKey': private_key
        })

        if (socks_host is None and socks_port is not None) or (
                socks_host is not None and socks_port is None):
            raise Exception('Socks port or socks host is not provided')

        if socks_host is not None:
            connection_args_dict.update({
                'socks_host': socks_host,
                'socks_port': socks_port
            })

        try:
            connection = Connection(target_ip, **connection_args_dict)

            request = NodeJoin(target_port, username, app_log=app_log)
            message = Message(MessageType.NodeJoin3, private_key, request, **message_args_dict)
            res = connection.fetch(message)
            print(res.to_json())
        except:
            print('Skipped {}'.format(target_ip))
            pass

    for i in ips:
        st = Thread(target=call, args=[i])
        st.start()
        st.join(timeout=1)  # configure
        stop_it.set()


propagate('217.23.6.40', 1080)
#
#
# propagate('verifier1.nyzo.co', '178.197.249.213', 1080)
# propagate('verifier2.nyzo.co', '178.197.249.213', 1080)
# propagate('verifier3.nyzo.co', '178.197.249.213', 1080)
# propagate('verifier4.nyzo.co', '178.197.2449.213', 1080)
# propagate('verifier5.nyzo.co', '178.197.248.213', 1080)
# propagate('verifier6.nyzo.co', '178.197.2448.213', 1080)
# propagate('verifier7.nyzo.co', '178.197.2448.213', 1080)
# propagate('verifier8.nyzo.co', '178.197.244448.213', 1080)
# propagate('verifier9.nyzo.co', '178.197.248.213', 1080)
