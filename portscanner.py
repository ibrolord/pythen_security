import argparse, sys, socket, threading

screen_lock = threading.Semaphore()

def connScan(tgtHost, tgtPort):
    try:
        connSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connSocket.connect((tgtHost,tgtPort))
        connSocket.send(b'Recon stuff \r\n')
        results = connSocket.recv(100)
        screen_lock.acquire()
        print(f"[+] {tgtPort}/tcp open")
        print(f"[+] {str(results)}")
        connSocket.close()

    except Exception as e:
        screen_lock.acquire()
        print(f"[-] {tgtPort}/tcp close")
        print(f"[-] {e} for port {tgtPort}")
    finally:
        screen_lock.release()
        connSocket.close()

def portScan(tgtHost, tgtPorts):
    try:
        tgtIP = socket.gethostbyname(tgtHost)
    except:
        print(f"[-] Cannot resolve {tgtHost}: Unknown Host")
        return

    try:
        tgtName = socket.gethostbyaddr(tgtIP)
        print(f"[+] Scan Results for: {tgtName[0]}")
    except:
        print(f"[+] Scan Results for: {tgtIP}")
    
    socket.setdefaulttimeout(1)

    for tgtPort in tgtPorts:
        t = threading.Thread(target=connScan, args=(tgtHost, int(tgtPort)))
        t.start()


def main():
    parser = argparse.ArgumentParser(usage=f'usage {sys.argv[0]} -H <target host> -p <target port> \nexample: python3 {sys.argv[0]} -H 10.0.0.69 -p 69,96')

    parser.add_argument('-H', type=str, required=True, dest='tgtHost', help='Specify target host')
    parser.add_argument('-p', type=str, required=True, help='Specify target ports (seperated by comma, no spaces)', dest='tgtPort')

    args = parser.parse_args()

    tgtHost = args.tgtHost
    tgtPorts = str(args.tgtPort).split(',')

    portScan(tgtHost, tgtPorts)

main()