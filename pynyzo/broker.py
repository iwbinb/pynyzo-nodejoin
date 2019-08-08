import asyncio
from proxybroker import Broker

async def save(proxies, filename):
    """Save proxies to a file."""
    with open(filename, 'w') as f:
        while True:
            proxy = await proxies.get()
            if proxy is None:
                break
            row = '%s:%d\n' % (proxy.host, proxy.port)
            f.write(row)

def main():
    proxies = asyncio.Queue()
    broker = Broker(proxies)
    tasks = asyncio.gather(broker.find(types=['SOCKS5', 'SOCKS4'], limit=100),
                           save(proxies, filename='proxies.txt'))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)


if __name__ == '__main__':
    main()


# def make_verifiers():
#     get_write(get())
#
#
# if __name__ == '__main__':
#     make_verifiers()
