import nmap

def scan():
    nm = nmap.PortScanner()

    net_scan = nm.scan('192.168.0.1/24')

    hosts = nm.all_hosts()
    vendors_list = [nm[host]['vendor'] for host in hosts]

    return {k:v for element in vendors_list for k,v in element.items()}
    # return [nm[host]['vendor'] for host in hosts]


if __name__ == '__main__':
    hosts = scan()
    for host in hosts:
        print(host)
