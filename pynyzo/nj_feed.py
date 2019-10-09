from redis import Redis
from rq import Queue
from node_join_func import propagate
q = Queue('ipflow', connection=Redis())

def test_proxy(ip):
    print('testing proxy {}'.format(ip))
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
        ip_s = ip.split(':')
        ip = ip_s[0]
        port = ip_s[1]
        if test_proxy(ip):
            # q.enqueue(propagate, args=(ip, 1080), job_timeout=86400)
            q.enqueue(propagate, args=(ip, port), job_timeout=86400)

if __name__ == '__main__':
    get_list()
