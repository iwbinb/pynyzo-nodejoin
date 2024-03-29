# from node_join_func import propagate

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

def test_one():
    import subprocess
    from threading import Thread, Event
    import time
    stop_it = Event()
    kl = keys_list()
    il = ips_list()
    kl = kl[4]

    key = kl[1]
    print('Using private key {}'.format(str(key)))
    port = kl[0]
    port = 63190
    host = '104.238.97.230'
    nport = 9444
    user = 'xantyp' + str(port)

    def call(ip):
        print('Propagating with IP {} to {}'.format(host, ip))
        propagate(ip, user, host, port, key)

    for i in il:
        st = Thread(target=call, args=[i])
        st.start()
        st.join(timeout=1.2)  # configure
        stop_it.set()

# test_one()
ips_list()
