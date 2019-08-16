from redis import Redis
from rq import Queue
from node_join_func import propagate
q = Queue('ipflow', connection=Redis())

def test_proxy(ip):
    import socks
    try:
        sock = socks.socksocket()
        sock.set_proxy(socks.SOCKS5, ip, 1080)
        sock.settimeout(2)
        sock.connect(('www.google.com', 80))
    except:
        return False
    else:
        return True
    finally:
        sock.close()


def get_list():
    print('start')
    with open('data/ips', 'r') as f:
        ip_list = []
        for line in f:
            ip_list.append(line.strip())

    for ip in ip_list:
        print(ip)
        if test_proxy(ip[:5]):
            q.enqueue(propagate, (ip, 1080))

get_list()
