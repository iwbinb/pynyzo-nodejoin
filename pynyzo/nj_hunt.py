import asyncio
from proxybroker import Broker
from redis import Redis
from rq import Queue
from node_join_func import propagate

q = Queue('ipflow', connection=Redis())

def add_ip(host, port):
    with open('data/ips', 'a') as f:
        f.write('{}:{}\n'.format(host, port))

async def show(proxies):
    while True:
        proxy = await proxies.get()
        if proxy is None: break
        add_ip(proxy.host, proxy.port)
        print('Added IP to file and queue: {}:{}'.format(proxy.host, proxy.port))
        q.enqueue(propagate, args=(proxy.host, proxy.port), job_timeout=86400)


proxies = asyncio.Queue()
broker = Broker(proxies)
tasks = asyncio.gather(broker.find(types=['SOCKS4', 'SOCKS5'], limit=10000), show(proxies))

loop = asyncio.get_event_loop()
loop.run_until_complete(tasks)
