import asyncio
from proxybroker import Broker

async def show(proxies):
    while True:
        proxy = await proxies.get()
        if proxy is None: break
        print('Found proxy: %s' % proxy)

proxies = asyncio.Queue()
broker = Broker(proxies)
tasks = asyncio.gather(
    broker.find(types=['SOCKS5', 'SOCKS4'], limit=1000),
    show(proxies))

loop = asyncio.get_event_loop()
loop.run_until_complete(tasks)
