def keys_list():
    with open('test2.txt', 'r') as f:
        l = f.readlines()
        keys = [i.rstrip() for i in l]
        keys_with_port = []
        count = 0
        for i in range(10000, 10000+len(keys)):
            tl = [i, keys[count]]
            count += 1
            keys_with_port.append(tl)

        return keys_with_port

def ips_list():
    import requests
    # res = requests.get('http://95.216.184.40/nodes.txt')
    res = requests.get('http://94.130.179.46/nyzo.html')
    res = res.content.decode('utf-8')
    res = res.split('<tr>')
    ip_list = ['94.130.179.46', 'verifier0.nyzo.co', 'verifier1.nyzo.co', 'verifier2.nyzo.co', 'verifier3.nyzo.co', 'verifier4.nyzo.co', 'verifier5.nyzo.co', 'verifier6.nyzo.co', 'verifier7.nyzo.co', 'verifier8.nyzo.co', 'verifier9.nyzo.co']
    for i in res:
        r = i.split('</td>')
        try:
            if 'In Cycle' in r[6]:
                ip = r[0].split('>')
                ip = ip[len(ip)-1]
                print(ip)
                ip_list.append(ip)
                print(len(ip_list))
        except:
            pass
    return ip_list

def test_one():
    import subprocess
    from threading import Thread, Event
    import time
    stop_it = Event()
    kl = keys_list()
    il = ips_list()
    kl = kl[4]

    key = kl[1]
    port = kl[0]
    port = 9050
    host = '127.0.0.1'
    host = '104.200.20.46'
    nport = 9444
    user = 'xantyp' + str(port)

    def call(ip):
        subprocess.call(
            ['python3', 'node_join.py', '--ip', str(i), '--port', str(nport), '--user', str(user), '--socks_host',
             str(host), '--socks_port', str(port), '--private_key', str(key)])

    for i in il:
        st = Thread(target=call, args=[i])
        st.start()
        st.join(timeout=5)
        stop_it.set()

test_one()
#ips_list()
